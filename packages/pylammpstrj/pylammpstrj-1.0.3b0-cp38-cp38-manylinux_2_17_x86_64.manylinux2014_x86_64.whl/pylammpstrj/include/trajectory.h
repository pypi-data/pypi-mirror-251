#ifndef _TRAJECTORY_H
#define _TRAJECTORY_H
#include "atom.h"
#include "box.h"
#include "utils.h"

#include <stdbool.h>
#include <stdio.h>

/** Parameters for atoms selection. */
typedef struct SelectionParameters
{
    unsigned int field;
    enum Operator op;
    union AtomField value;
} selection_parameters;

#define FILE_NAME_LIMIT FILENAME_MAX

/** Trajectory file structure. */
struct TrajectoryFile
{
    char file_name[FILE_NAME_LIMIT];
    char user_format[BUFFER_LIMIT];
    unsigned int batch_size;
    unsigned long N_configurations;
    unsigned long *steps;
    long *conf_pos;
    unsigned int N_selections;
    selection_parameters *parameters;
};

/** Creating a `TrajectoryFile`. */
struct TrajectoryFile trajectoryfile_new(const char *file_name,
                                         const char *user_format,
                                         const unsigned int batch_size);

/** Copying a `TrajectoryFile` to another. */
struct TrajectoryFile trajectoryfile_copy(struct TrajectoryFile *dest,
                                          const struct TrajectoryFile src);

/** Deleting a `TrajectoryFile`. */
void trajectoryfile_delete(struct TrajectoryFile *trajectory_file);

/**
 * To compute the average of a property over the configurations.
 */
double *trajectoryfile_average_property(
    const struct TrajectoryFile trajectory_file, const unsigned int field);

/** Stores atoms selection parameters. */
void trajectoryfile_select_atoms(struct TrajectoryFile *trajectory_file,
                                 const unsigned int field,
                                 const enum Operator op,
                                 const union AtomField value);

/** The data structure used to represent a trajectory. */
struct Trajectory
{
    struct AtomBuilder atom_builder;
    unsigned long N_configurations;
    unsigned int *N_atoms;
    unsigned int *steps;
    struct Box *box;
    struct Atom *atoms;
};

/** Creating a `Trajectory` from a `TrajectoryFile`. */
void trajectoryfile_read_slice(struct TrajectoryFile trajectory_file,
                               unsigned long start,
                               unsigned long N_configurations,
                               struct Trajectory *trajectory);

void trajectory_init(struct Trajectory *trajectory,
                     const struct AtomBuilder atom_builder,
                     const unsigned long N_configurations,
                     unsigned int *N_atoms, unsigned int *steps,
                     struct Box *box, struct Atom *atoms);

void trajectory_skip(FILE **input, const unsigned long start);

void trajectory_read(const char *file_name, const unsigned long start,
                     const char *user_format, struct Trajectory *trajectory);

/**
 * Select atoms from a group of atoms based on a condition over one of their
 * properties.
 *
 * @param[in] N_atoms the number of atoms in the input array.
 * @param[in] atoms the input `Atom` array.
 * @param[in] select the selection function.
 * @param[in] value the value to which the atoms property is compared.
 * @param[out] the number of selected atoms.
 *
 * @return an array of `Atom`s of size `N_selected`.
 *
 * @sa {lower_than .. greater_than}.
 */
void select_atoms(struct Trajectory *trajectory, const unsigned int field,
                  const enum Operator op, const union AtomField value,
                  const bool inplace, struct Trajectory *selected);

/**
 * To compute the average of a property over the configurations.
 */
double *trajectory_average_property(const struct Trajectory,
                                    const unsigned int);

/**
 * Deletes a `Trajectory`.
 */
void trajectory_delete(struct Trajectory *trajectory);

#endif
