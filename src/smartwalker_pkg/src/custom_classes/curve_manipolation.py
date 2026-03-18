#!/usr/bin/env python3

import numpy as np
from . import csv_handler as ch

def parametric_guide(type, start_point, end_point, A, num, M_t = None):

    # return gamma
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y
    P0 = np.array([x0, y0], dtype = float)
    P1 = np.array([x1, y1], dtype = float)
    v = P1 - P0
    L = np.linalg.norm(v)
    t =  v/L
    n = np.array([-t[1], t[0]])
    s = np.linspace(0,1, num)

    match type:
        case 0:
            gamma = P0.reshape(2,1) + t.reshape(2,1)*s*L
        case 1:
            R = L/2
            C = (P0+P1)/2
            theta0 = np.arctan2(P0[1] - C[1], P0[0] - C[0])
            theta = theta0 + s*2*np.pi
            gamma = np.vstack((C[0] + R * np.cos(theta),
                               C[1] + R * np.sin(theta)))
            gamma = gamma[:, 500:-500]
        case 2:
            gamma = (P0.reshape(2,1)
                     + t.reshape(2,1) * s * L
                     + n.reshape(2,1) * (A * np.sin(2*np.pi*s)))
        case 3:
            #Leggere da file csv la lista di punti.
            _, x, y = ch.read_from_csv_two_values("custom", "")

            s_original = np.linspace(0,1,len(x))
            fx = np.interp(s, s_original, x)
            fy = np.interp(s, s_original, y)

            gamma = np.vstack((
                fx,
                fy,
            ))

    if M_t is not None:
        gamma = np.vstack((gamma, np.ones(gamma.shape[1])))
        guide_transformed = M_t @ gamma
        return gamma, guide_transformed
    return gamma

def calculate_errors(gamma, robot, Emax, delta):

    # Calcolo vettore normale normalizzato
    _, n = compute_tangent_normal(gamma)

    errors = np.zeros(robot.shape[1])
    index_before = 0
    # VEDI READ.ME -> "Calcolo accuratezza"
    for i in range(robot.shape[1]):
        p = robot[:, i].reshape(3,1)
        dist = np.linalg.norm(p - gamma, axis=0)
        s = np.argmin(dist)
        if s >= index_before:
            diff = robot[:-1, i] - gamma[:-1, s]
            err = abs(diff @ n[:,s].reshape(2,1)) - delta
            errors[i] = max(err, 0.0)
            index_before = s
    print(f"error: {errors}")
    N = len(errors)
    rmse = np.sqrt(1.0 / N * np.sum(errors ** 2.0))
    accuracy = 100 * (1.0 - rmse / Emax)
    if accuracy < 0:
        accuracy = 0
    return accuracy

def compute_tangent_normal(gamma):
    dgamma = np.diff(gamma, axis=1)
    norms = np.linalg.norm(dgamma, axis=0)

    # evita divisioni per zero
    valid = norms > 1e-9
    t = np.zeros_like(dgamma)
    t[:, valid] = dgamma[:, valid] / norms[valid]

    # usa ultima tangente per allineare dimensioni
    t = np.hstack((t, t[:, -1:]))
    n = np.vstack((-t[1, :], t[0, :]))

    return t, n

def get_band_area(curve, delta):
    # Utilizzato principalemnte per le guida sinusoidale, circolare e personalizzata.
    _, n_gamma = compute_tangent_normal(curve)
    upper = curve + delta * n_gamma
    lower = curve - delta * n_gamma

    poly_x = np.concatenate([upper[0], lower[0][::-1]])
    poly_y = np.concatenate([upper[1], lower[1][::-1]])
    return poly_x, poly_y






