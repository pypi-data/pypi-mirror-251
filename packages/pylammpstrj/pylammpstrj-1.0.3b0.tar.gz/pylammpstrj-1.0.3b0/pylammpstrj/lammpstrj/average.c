#include "trajectory.h"

#include <errno.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static double *compute_average(const size_t offset,
                               const enum AtomFieldType type,
                               const struct Trajectory trajectory)
{
    double *averages = calloc(trajectory.N_configurations, sizeof(double));
    if (averages == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (compute_average.averages)");
        return NULL;
    }

    for (unsigned int c = 0, i = 0; c < trajectory.N_configurations; c++)
    {
        for (unsigned int a = 0; a < trajectory.N_atoms[c]; a++, i++)
        {
            switch (type)
            {
                case AFT_INT:
                    averages[c] += (double) *(
                        int *) ((void *) (trajectory.atoms + i) + offset);
                    break;
                case AFT_DOUBLE:
                    averages[c] +=
                        *(double *) ((void *) (trajectory.atoms + i) + offset);
                    break;
                default:
                    free(averages);
                    averages = NULL;
                    errno = EINVAL;
                    perror("Error while selecting type of value");
                    return NULL;
            }
        }
        averages[c] /= trajectory.N_atoms[c];
    }

    return averages;
}

static double *compute_average_additional(const size_t offset,
                                       const enum AtomFieldType type,
                                       const struct Trajectory trajectory)
{
    double *averages = calloc(trajectory.N_configurations, sizeof(double));
    if (averages == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (compute_average.averages)");
        return NULL;
    }

    for (unsigned int c = 0, i = 0; c < trajectory.N_configurations; c++)
    {
        for (unsigned int a = 0; a < trajectory.N_atoms[c]; a++, i++)
        {
            switch (type)
            {
                case AFT_INT:
                    averages[c] += (double) trajectory.atoms[i]
                                          .additionnal_fields[offset]
                                          .i;
                    break;
                case AFT_DOUBLE:
                    averages[c] +=
                        trajectory.atoms[i].additionnal_fields[offset].d;
                    break;
                default:
                    free(averages);
                    errno = EINVAL;
                    perror("Error while selecting type of value");
                    return NULL;
            }
        }
        averages[c] /= trajectory.N_atoms[c];
    }

    return averages;
}

double *trajectory_average_property(const struct Trajectory trajectory,
                                    const unsigned int field)
{
    // Preparing the array
    double *averages;

    // Transforming the field into an offset
    size_t offset = trajectory.atom_builder.offsets[field];

    // Getting the type of data
    enum AtomFieldType type = trajectory.atom_builder.fields_types[field];

    if (!trajectory.atom_builder.is_additional[field])
    {
        averages = compute_average(offset, type, trajectory);
        if (errno != 0) return NULL;
    }
    else
    {
        averages = compute_average_additional(offset, type, trajectory);
        if (errno != 0) return NULL;
    }

    return averages;
}

double *trajectoryfile_average_property(
    const struct TrajectoryFile trajectory_file, const unsigned int field)
{
    // Initializing
    struct Trajectory tmp_trajectory;
    trajectoryfile_read_slice(trajectory_file, 0, 1, &tmp_trajectory);
    if (errno != 0)
    {
        perror(
            "Error while initializing a trajectory "
            "(trajectoryfile_average_property.tmp_trajectory)");
        return NULL;
    }

    // Preparing the array
    double *averages = calloc(trajectory_file.N_configurations, sizeof(double));
    if (averages == NULL)
    {
        errno = ENOMEM;
        perror(
            "Error while allocating memory "
            "(compute_average_property.averages)");
        return NULL;
    }

    // Transforming the field into an offset
    size_t offset = tmp_trajectory.atom_builder.offsets[field];

    // Getting the type of data
    enum AtomFieldType type = tmp_trajectory.atom_builder.fields_types[field];

    // Preparing to read
    unsigned int N_batches = (unsigned int) floor(
        (double) trajectory_file.N_configurations / trajectory_file.batch_size);
    unsigned int remaining_conf = trajectory_file.N_configurations % trajectory_file.batch_size;

    if (!tmp_trajectory.atom_builder.is_additional[field])
    {
        for (unsigned int batch = 0; batch < N_batches; batch++)
        {
            struct Trajectory trajectory;
            trajectoryfile_read_slice(
                trajectory_file,
                trajectory_file.steps[batch * trajectory_file.batch_size],
                trajectory_file.batch_size, &trajectory);
            if (errno != 0)  // Could not read slice
            {
                free(averages);
                perror(
                    "Error while reading a slice "
                    "(trajectoryfile_average_property.trajectory)");
                return NULL;
            }

            double *tmp = compute_average(offset, type, trajectory);
            memcpy(averages + batch * trajectory_file.batch_size, tmp, trajectory_file.batch_size * sizeof(double));
            free(tmp);
            trajectory_delete(&trajectory);
        }

        if (remaining_conf != 0)
        {
            struct Trajectory trajectory;
            trajectoryfile_read_slice(
                trajectory_file,
                trajectory_file.steps[N_batches * trajectory_file.batch_size],
                remaining_conf, &trajectory);
            if (errno != 0)  // Could not read slice
            {
                free(averages);
                perror(
                    "Error while reading a slice "
                    "(trajectoryfile_average_property.trajectory)");
                return NULL;
            }

            double *tmp = compute_average(offset, type, trajectory);
            memcpy(averages + N_batches * trajectory_file.batch_size, tmp, remaining_conf * sizeof(double));
            free(tmp);
            trajectory_delete(&trajectory);
        }
    }
    else
    {
        for (unsigned int batch = 0; batch < N_batches; batch++)
        {
            struct Trajectory trajectory;
            trajectoryfile_read_slice(
                trajectory_file,
                trajectory_file.steps[batch * trajectory_file.batch_size],
                trajectory_file.batch_size, &trajectory);
            if (errno != 0)  // Could not read slice
            {
                free(averages);
                perror(
                    "Error while reading a slice "
                    "(trajectoryfile_average_property.trajectory)");
                return NULL;
            }

            double *tmp = compute_average_additional(offset, type, trajectory);
            memcpy(averages + batch * trajectory_file.batch_size, tmp, trajectory_file.batch_size * sizeof(double));
            free(tmp);
            trajectory_delete(&trajectory);
        }

        if (remaining_conf != 0)
        {
            struct Trajectory trajectory;
            trajectoryfile_read_slice(
                trajectory_file,
                trajectory_file.steps[N_batches * trajectory_file.batch_size],
                remaining_conf, &trajectory);
            if (errno != 0)  // Could not read slice
            {
                free(averages);
                perror(
                    "Error while reading a slice "
                    "(trajectoryfile_average_property.trajectory)");
                return NULL;
            }

            double *tmp = compute_average_additional(offset, type, trajectory);
            memcpy(averages + N_batches * trajectory_file.batch_size, tmp, remaining_conf * sizeof(double));
            free(tmp);
            trajectory_delete(&trajectory);
        }
    }

    trajectory_delete(&tmp_trajectory);
    return averages;
}
