# ----------------------------------------------------------------------------
# Copyright (c) 2016--, taxster development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import division

from collections import Counter, defaultdict


def uc_consensus_assignments(uc, taxonomy_map, min_consensus_fraction=0.51,
                             unassignable_label="Unassigned"):
    """ Compute consensus taxonomic annotations for a uc file

        Parameters
        ----------
        uc : file-like object
            A .uc file, such as those generated by uclust, usearch, or vsearch
        taxonomy_map : dict
            Mapping of target sequence identifiers to taxonomic annotations
        min_consensus_fraction : float, optional
            The minimum fraction of the annotations that a specfic annotation
            must be present in for that annotation to be accepted. This must
            be greater than 0.50.
        unassignable_label : str, optional
            The label to apply if no acceptable annotations are identified.

        Returns
        -------
        dict of tuples
            Keys are query identifiers, and values are tuples of consensus
            taxonomic annotation (list), consensus fraction (float), and number
            of input annotations that were provided for the query (int).

        Raises
        ------
        ValueError
            If min_consensus_fraction <= 0.50.

        Notes
        -----
        The .uc format is documented in [1]_. This format was initally defined
        by Robert Edgar [2]_. This is not an implementation of utax [3]_, but
        rather just an approach for using search hits to identify taxonomy.

        This algorithm was originally described in Bokulich et al. (in
        preparation) [4]_.

        References
        ----------
        [1] http://drive5.com/usearch/manual/opt_uc.html
        [2] http://drive5.com/
        [3] http://drive5.com/usearch/manual/utax_algo.html
        [4] https://peerj.com/preprints/934/

    """
    annotations = _uc_to_taxonomy(uc, taxonomy_map)
    return _compute_consensus_annotations(annotations, min_consensus_fraction,
                                          unassignable_label)


def _uc_to_taxonomy(uc, taxonomy_map):
    """ Process a uc file and associated taxonomy annotations

        Parameters
        ----------
        uc : file-like object
            A .uc file, such as those generated by uclust, usearch, or vsearch
        taxonomy_map : dict
            Mapping of target sequence identifiers to taxonomic annotations

        Returns
        -------
        dict
            Mapping of query sequence identifiers to taxonomic annotations
            of corresponding hits.

        Notes
        -----
        The .uc format is documented in [1]_. This format was initally defined
        by Robert Edgar [2]_. This is not an implementation of utax [3]_, but
        rather just an approach for using search hits to identify taxonomy.

        References
        ----------
        [1] http://drive5.com/usearch/manual/opt_uc.html
        [2] http://drive5.com/
        [3] http://drive5.com/usearch/manual/utax_algo.html

    """
    # This code has been ported to taxster from QIIME 1.9.1 with
    # permission from @gregcaporaso.
    results = defaultdict(list)
    for line in uc:
        line = line.strip()
        if line.startswith('#') or line == "":
            continue
        elif line.startswith('H'):
            fields = line.split('\t')
            query_id = fields[8].split()[0]
            subject_id = fields[9].split()[0]
            tax = taxonomy_map[subject_id]
            results[query_id].append(tax)
        elif line.startswith('N'):
            fields = line.split('\t')
            query_id = fields[8].split()[0]
            results[query_id].append([])
    return results


def _compute_consensus_annotations(query_annotations, min_consensus_fraction,
                                   unassignable_label):
    """
        Parameters
        ----------
        query_annotations : dict of lists
            Keys are query identifiers, and values are lists of all
            taxonomic annotations associated with that identfier.

        Returns
        -------
        dict
            Keys are query identifiers, and values are the consensus of the
            input taxonomic annotations.

    """
    # This code has been ported to taxster from QIIME 1.9.1 with
    # permission from @gregcaporaso.
    result = {}
    for query_id, annotations in query_annotations.items():
        consensus_annotation, consensus_fraction = \
            _compute_consensus_annotation(annotations, min_consensus_fraction,
                                          unassignable_label)
        result[query_id] = (consensus_annotation, consensus_fraction,
                            len(annotations))
    return result


def _compute_consensus_annotation(annotations, min_consensus_fraction,
                                  unassignable_label):
    """ Compute the consensus of a collection of annotations

        Parameters
        ----------
        annotations : list of lists
            Taxonomic annotations to compute the consensus of.
        min_consensus_fraction : float
            The minimum fraction of the annotations that a specfic annotation
            must be present in for that annotation to be accepted. This must
            be greater than or equal to 0.51.
        unassignable_label : str
            The label to apply if no acceptable annotations are identified.

        Result
        ------
        consensus_annotation
            List containing the consensus assignment
        consensus_fraction
            Fraction of input annotations that agreed at the deepest
            level of assignment
    """
    # This code has been ported to taxster from QIIME 1.9.1 with
    # permission from @gregcaporaso.
    if min_consensus_fraction <= 0.5:
        raise ValueError("min_consensus_fraction must be greater than 0.5.")
    num_input_annotations = len(annotations)
    consensus_annotation = []

    # if the annotations don't all have the same number
    # of levels, the resulting annotation will have a max number
    # of levels equal to the number of levels in the assignment
    # with the fewest number of levels. this is to avoid
    # a case where, for example, there are n assignments, one of
    # which has 7 levels, and the other n-1 assignments have 6 levels.
    # A 7th level in the result would be misleading because it
    # would appear to the user as though it was the consensus
    # across all n assignments.
    num_levels = min([len(a) for a in annotations])

    # iterate over the assignment levels
    for level in range(num_levels):
        # count the different taxonomic assignments at the current level.
        # the counts are computed based on the current level and all higher
        # levels to reflect that, for example, 'p__A; c__B; o__C' and
        # 'p__X; c__Y; o__C' represent different taxa at the o__ level (since
        # they are different at the p__ and c__ levels).
        current_level_annotations = \
            Counter([tuple(e[:level + 1]) for e in annotations])
        # identify the most common taxonomic assignment, and compute the
        # fraction of annotations that contained it. it's safe to compute the
        # fraction using num_assignments because the deepest level we'll
        # ever look at here is num_levels (see above comment on how that
        # is decided).
        tax, max_count = current_level_annotations.most_common(1)[0]
        max_consensus_fraction = max_count / num_input_annotations
        # check whether the most common taxonomic assignment is observed
        # in at least min_consensus_fraction of the sequences
        if max_consensus_fraction >= min_consensus_fraction:
            # if so, append the current level only (e.g., 'o__C' if tax is
            # 'p__A; c__B; o__C', and continue on to the next level
            consensus_annotation.append((tax[-1], max_consensus_fraction))
        else:
            # if not, there is no assignment at this level, and we're
            # done iterating over levels
            break

    # construct the results
    # determine the number of levels in the consensus assignment
    consensus_annotation_depth = len(consensus_annotation)
    if consensus_annotation_depth > 0:
        # if it's greater than 0, generate a list of the
        # taxa assignments at each level
        annotation = [a[0] for a in consensus_annotation]
        # and assign the consensus_fraction_result as the
        # consensus fraction at the deepest level
        consensus_fraction_result = \
            consensus_annotation[consensus_annotation_depth - 1][1]
    else:
        # if there are zero assignments, indicate that the taxa is
        # unknown
        annotation = [unassignable_label]
        # and assign the consensus_fraction_result to 1.0 (this is
        # somewhat arbitrary, but could be interpreted as all of the
        # assignments suggest an unknown taxonomy)
        consensus_fraction_result = 1.0

    return annotation, consensus_fraction_result