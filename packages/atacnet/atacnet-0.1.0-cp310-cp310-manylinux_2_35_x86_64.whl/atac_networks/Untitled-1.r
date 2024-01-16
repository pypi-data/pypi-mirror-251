find_distance_parameter <- function(dist_mat,
                       gene_range,
                       maxit,
                       null_rho,
                       s,
                       distance_constraint,
                       distance_parameter_convergence) {
  if (sum(dist_mat > distance_constraint)/2 < 1) {
    return("No long edges")
  }

  found <- FALSE
  starting_max <- 2
  distance_parameter <- 2
  distance_parameter_max <- 2
  distance_parameter_min <- 0
  it <- 0
  while(found != TRUE & it < maxit) {
    vals <- as.matrix(exprs(gene_range))
    cov_mat <- cov(t(vals))
    diag(cov_mat) <- diag(cov_mat) + 1e-4

    rho <- get_rho_mat(dist_mat, distance_parameter, s)

    GL <- glasso::glasso(cov_mat, rho)
    big_entries <- sum(dist_mat > distance_constraint)

    print(GL$wi[1:5, 1:5])
    print(distance_parameter)
    if (((sum(GL$wi[dist_mat > distance_constraint] != 0)/big_entries) > 0.05) |
        (sum(GL$wi == 0)/(nrow(GL$wi)^2) < 0.2 ) ) {
      longs_zero <- FALSE
    } else {
      longs_zero <- TRUE
    }

    if (longs_zero != TRUE | (distance_parameter == 0)) {
      distance_parameter_min <- distance_parameter
    } else {
      distance_parameter_max <- distance_parameter
    }
    new_distance_parameter <- (distance_parameter_min +
                                 distance_parameter_max)/2

    if(new_distance_parameter == starting_max) {
      new_distance_parameter <- 2 * starting_max
      starting_max <- new_distance_parameter
    }

    if (distance_parameter_convergence > abs(distance_parameter -
                                             new_distance_parameter)) {
      found <- TRUE
    } else {
      distance_parameter <- new_distance_parameter
    }
    it <- it + 1
  }
  if (maxit == it) warning("maximum iterations hit")
  return(distance_parameter)
}