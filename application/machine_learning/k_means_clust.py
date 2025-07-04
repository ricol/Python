#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''README, Author - Anurag Kumar(mailto:anuragkumarak95@gmail.com)

Requirements:
  - sklearn
  - numpy
  - matplotlib

Python:
  - 3.5

Inputs:
  - X , a 2D numpy array of features.
  - k , number of clusters to create.
  - initial_centroids , initial centroid values generated by utility function(mentioned in usage).
  - maxiter , maximum number of iterations to process.
  - heterogeneity , empty list that will be filled with hetrogeneity values if passed to kmeans func.

Usage:
  1. define 'k' value, 'X' features array and 'hetrogeneity' empty list

  2. create initial_centroids,
        initial_centroids = get_initial_centroids(
            X, 
            k, 
            seed=0 # seed value for initial centroid generation, None for randomness(default=None)
            )

  3. find centroids and clusters using kmeans function.

        centroids, cluster_assignment = kmeans(
            X, 
            k, 
            initial_centroids, 
            maxiter=400,
            record_heterogeneity=heterogeneity, 
            verbose=True # whether to print logs in console or not.(default=False)
            )

  4. Plot the loss function, hetrogeneity values for every iteration saved in hetrogeneity list.
        plot_heterogeneity(
            heterogeneity, 
            k
        )

  5. Have fun..

'''
from __future__ import print_function
import numpy as np
from sklearn.metrics import pairwise_distances

TAG = 'K-MEANS-CLUST/ '

def get_initial_centroids(data, k, seed=None):
    '''Randomly choose k data points as initial centroids'''
    if seed is not None: # useful for obtaining consistent results
        np.random.seed(seed)
    n = data.shape[0] # number of data points

    # Pick K indices from range [0, N).
    rand_indices = np.random.randint(0, n, k)

    # Keep centroids as dense format, as many entries will be nonzero due to averaging.
    # As long as at least one document in a cluster contains a word,
    # it will carry a nonzero weight in the TF-IDF vector of the centroid.
    centroids = data[rand_indices, :]

    return centroids

def centroid_pairwise_dist(X, centroids):
    return pairwise_distances(X, centroids, metric='euclidean')

def assign_clusters(data, centroids):

    # Compute distances between each data point and the set of centroids:
    # Fill in the blank (RHS only)
    distances_from_centroids = centroid_pairwise_dist(data, centroids)

    # Compute cluster assignments for each data point:
    # Fill in the blank (RHS only)
    cluster_assignment = np.argmin(distances_from_centroids, axis=1)

    return cluster_assignment

def revise_centroids(data, k, cluster_assignment):
    new_centroids = []
    for i in range(k):
        # Select all data points that belong to cluster i. Fill in the blank (RHS only)
        member_data_points = data[cluster_assignment == i]
        # Compute the mean of the data points. Fill in the blank (RHS only)
        centroid = member_data_points.mean(axis=0)
        new_centroids.append(centroid)
    new_centroids = np.array(new_centroids)

    return new_centroids

def compute_heterogeneity(data, k, centroids, cluster_assignment):

    heterogeneity = 0.0
    for i in range(k):

        # Select all data points that belong to cluster i. Fill in the blank (RHS only)
        member_data_points = data[cluster_assignment == i,:]

        if member_data_points.shape[0] > 0: # check if i-th cluster is non-empty
            # Compute distances from centroid to data points (RHS only)
            distances = pairwise_distances(member_data_points, [centroids[i]], metric='euclidean')
            squared_distances = distances ** 2
            heterogeneity += np.sum(squared_distances)

    return heterogeneity

from matplotlib import pyplot as plt
def plot_heterogeneity(heterogeneity, k):
    plt.figure(figsize=(7, 4))
    plt.plot(heterogeneity, linewidth=4)
    plt.xlabel('# Iterations')
    plt.ylabel('Heterogeneity')
    plt.title('Heterogeneity of clustering over time, K={0:d}'.format(k))
    plt.rcParams.update({'font.size': 16})
    plt.show()

def kmeans(data, k, initial_centroids, maxiter=500, record_heterogeneity=None, verbose=False):
    '''This function runs k-means on given data and initial set of centroids.
       maxiter: maximum number of iterations to run.(default=500)
       record_heterogeneity: (optional) a list, to store the history of heterogeneity as function of iterations
                             if None, do not store the history.
       verbose: if True, print how many data points changed their cluster labels in each iteration'''
    centroids = initial_centroids[:]
    prev_cluster_assignment = None

    for itr in range(maxiter):        
        if verbose:
            print(itr, end='')

        # 1. Make cluster assignments using nearest centroids
        cluster_assignment = assign_clusters(data, centroids)

        # 2. Compute a new centroid for each of the k clusters, averaging all data points assigned to that cluster.
        centroids = revise_centroids(data, k, cluster_assignment)

        # Check for convergence: if none of the assignments changed, stop
        if prev_cluster_assignment is not None and \
            (prev_cluster_assignment == cluster_assignment).all():
                break

        # Print number of new assignments 
        if prev_cluster_assignment is not None:
            num_changed = np.sum(prev_cluster_assignment != cluster_assignment)
            if verbose:
                print('    {0:5d} elements changed their cluster assignment.'.format(num_changed))   

        # Record heterogeneity convergence metric
        if record_heterogeneity is not None:
            # YOUR CODE HERE
            score = compute_heterogeneity(data, k, centroids, cluster_assignment)
            record_heterogeneity.append(score)

        prev_cluster_assignment = cluster_assignment[:]

    return centroids, cluster_assignment

# Mock test below
if False: # change to true to run this test case.
    import sklearn.datasets as ds
    dataset = ds.load_iris()
    k = 3
    heterogeneity = []
    initial_centroids = get_initial_centroids(dataset['data'], k, seed=0)
    centroids, cluster_assignment = kmeans(dataset['data'], k, initial_centroids, maxiter=400,
                                           record_heterogeneity=heterogeneity, verbose=True)
    plot_heterogeneity(heterogeneity, k)