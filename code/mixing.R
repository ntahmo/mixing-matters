# Mixing Matters: reciprocal mixing examples in base R.
q <- c(HP=400, LP=200, HV=200, LV=300)
M_prop <- matrix(rep(q / sum(q), each=length(q)), nrow=length(q),
                 dimnames=list(names(q), names(q)))
epsilon <- 0.4
M_pref <- epsilon * diag(length(q)) + (1-epsilon) * M_prop
check_mixing <- function(M, q) {
  F <- sweep(M, 1, q, `*`)
  list(row_error=max(abs(rowSums(M)-1)),
       reciprocity_error=max(abs(F-t(F))),
       nonnegative=all(M>=0))
}
print(check_mixing(M_prop, q))
print(check_mixing(M_pref, q))

# Two-axis balanced affinity: illustrative construction.
activity <- c('H','L','H','L')
typology <- c('P','P','V','V')
theta_r <- 0.8; theta_m <- 1.2
W <- outer(q, q) / sum(q) * exp(
  theta_r * outer(activity, activity, `==`) +
  theta_m * outer(typology, typology, `==`))
a <- rep(1, length(q))
for (iter in 1:30000) {
  F <- W * outer(a, a)
  rs <- rowSums(F)
  if (max(abs(rs-q)/q) < 1e-12) break
  a <- a * sqrt(q/rs)
}
if (iter == 30000) stop('Balancing did not converge')
F <- W * outer(a, a)
M_two <- sweep(F, 1, q, `/`)
print(check_mixing(M_two, q))
