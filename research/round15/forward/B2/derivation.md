# B2 total Taylor bound on the matched closed cube action

The graph and link-Haar convention are frozen to B1. Let S=k*sum_(f=1)^6 x_f with x_f=Tr(U_face_f)/2, and O=product_f x_f. Then |S|<=M=6|k| and |O|<=1. For integer N>=0 with N+2>M,

R_N = M^(N+1)/(N+1)! / (1-M/(N+2))

bounds the entire exponential Taylor remainder in absolute value. Consequently E0[exp S] and E0[O exp S] lie within R_N of their exact total-degree Taylor integrals. Degree means total power of the common scalar k after substitution; it matches total action order before substitution, not a separate truncation of each face weight.

For spin n/2 and d=n+1, the face expansion coefficient is

a_n(k)=sum_(j>=0) d*k^(n+2j)/(2^(n+2j)*j!*(n+1+j)!).

The proven spherical gluing identity gives Z=sum_n d^-4*a_n(k)^6. Inserting one x_f differentiates that face coefficient once. Thus A_O=sum_n d^-4*(a_n'(k))^6. The derivative acts independently on six originally distinct face couplings before restricting them to the diagonal. A sixth derivative of Z along the common k coordinate would insert (sum_f x_f)^6 and is a different observable.

At total order N, the partition needs n<=floor(N/6); the inserted polynomial needs n<=floor(N/6)+1. All terms used are exact rationals. The product of six independent one-face partitions is precisely the n=0 term. It receives its own absolute global-action remainder R_N. Subtracting the two enclosed partitions therefore retains both errors; factorization cannot be disproved by subtracting truncated central values alone.

Every face has zero untilted Haar mean, so E0[S]=0 and Jensen gives Z>=1. The independent one-face product likewise has a product-Haar action with zero mean and partition>=1. Intersecting each Taylor enclosure with [1,infinity) is valid. All observable numerator signs and positive-denominator quotient corners are retained.

The declared target is k=1/4, expectation width strictly less than10^-12, and strictly positive partition excess over the product of six independent one-face partitions. Degrees0,6,12,18,24 are retained, including failures. A successful finite partition or moment comparison does not supply a physical transfer generator or a mass gap.

The executed widths decrease from12 at degree0 through approximately0.00799 and6.69*10^-8 to3.76*10^-14 and3.30*10^-21. Degrees0,6,12 fail the requested expectation width. Degrees18,24 pass. The partition excess is inconclusive at degrees0,6 and certified positive from degree12. At degree24 the expectation is approximately0.0010231163599225617; the partition excess has exact lower endpoint approximately2.459818024625245*10^-7. These rounded numbers are display values; acceptance uses the saved rational endpoints.

The backward researcher also supplied an analytic sign observation: for a common real nonzero k, Z-Zindependent=sum_(n>=1) d_n^-4*a_n(k)^6 is strictly positive because the n=1 coefficient is nonzero. The finite exact enclosure separately establishes a quantitative value at the requested fixture. Neither quantity is the connected six-face cumulant; the requested observable is the ordinary product expectation and the secondary diagnostic is a difference of partition functions.
