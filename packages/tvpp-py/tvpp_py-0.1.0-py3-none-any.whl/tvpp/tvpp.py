import pyperclip as pc
def amhgqn() :
    s = '''
    $A = \\frac{1}{n} \sum{x_i}$   
    $M = np.median(x[x>0]) $   
    $H = \\frac{n}{\\frac{1}{x_1}+...+\\frac{1}{x_n}}$    
    $Q = np.median(x[x>=M])$    
    $G = \sqrt[n]{x_1*x_2*...*x_n}$    
    $N = \sum{I_{H<=x_k<=Q}}$
        '''
    return pc.copy(s)
def lek_prep():
    s = '''
    $f(x,a,b) = abx^{a-1}(1-x^a)^{b-1}$    
    $L(x,\hat{a},\hat{b}) = a^nb^nx^{n(a-1)}(1-x^a)^{n(b-1)}$
    $\ln L(x,\hat{a},\hat{b}) = n\ln a+n\ln b+n(a-1)\ln x+n(b-1)\ln (1-x^a)$

    {$(\ln L)^`_a = - \\frac{nx^a(b-1)\log (x)}{1-x^a} + n \log (x) + \\frac{n}{a} = 0$    
    {$(\ln L)^`_b = \\frac{n}{b} + n \ln (1-x^a) = 0$    
    a =    
    b =    
    $E(x) = \int_0^1{xf(x)dx}$
    $\int^q_0{f(x) = quantile => q = (1-(1-x)^{\\frac{1}{b}})^{\\frac{1}{a}}}$
    '''
    return pc.copy(s)
def omega_var_m3():
    s = '''
    $N = 28$ $n = 6$    
    $var(\overline{x}) = \\frac{\sigma^2}{n}$    
    $\mu _3 (\overline{x}) = \\frac{\mu _3 (x)}{n^2}$
    $ \mu _3 (x) = \\frac {1}{N} \sum{(x_i-\overline{x})^3}$
    '''
    return pc.copy(s)
def omega_sr_std():
    s = '''
    $\overline
    {x} = \\frac
    {1}
    {n}\sum
    {\overline
    {x_i}
    n_i}$
    $\sigma = \sqrt
    {\sigma ^ 2} = \sqrt
    {d ^ 2 + \overline
    {\sigma ^ 2}}$
    $ \overline
    {\sigma ^ 2} = \\frac
    {1}
    {n} \sum
    {\sigma_j ^ 2
    n_j}$
    '''
    return pc.copy(s)
def omega_cov_corr():
    s = '''
    $cov(x,y) = \\frac{\sum{(x_i-\overline{x})(y_i-\overline(y)}}{n} , y>=...$    
    $\\rho = \\frac{cov(x,y)}{\sigma_x \sigma_y}$
    '''
    return pc.copy(s)
def omega_e_var():
    s = '''$ E(\hat{x}) = E(x) = \hat(x) = \\frac{1}{n}\sum{x_i}$    
    $var(\hat{x}) = \\frac{\sigma^2}{n} \\frac{N-n}{N-1}$'''
    return pc.copy(s)
def zapw():
    s = '''$ \sigma = n(\mu,...)[1] $ _$\\alpha = $   
$\\beta_0 = H_0 \mu$ _ $ \\beta_1 = H_1\mu$
$z = \\frac{\sqrt{n}(\overline{x} - \mu _{0})}{\sigma}$  ____ 
$A = N(0,1).isf (\\frac {\\alpha} {2})$ _____  
$P = 2*min(N(0,1).cdf(z),N(0,1).sf(z))$   
$W = 1-(\phi _0 (z_{\\frac{\\alpha}{2}} - \\frac{\sqrt{n}}{\sigma}$
$(\mu _1-\mu _0)+ \phi _0(z_{\\frac{alpha}{2}}+\\frac{sqrt{n}}{\sigma}$
$(\mu _1-\mu _0)))$'''
    return pc.copy(s)

def red_blue():
    s = '''$ X_i = 15R_i-7B_i$   
$\overline{x} = \\frac{1}{n}\sum{x_i}$  
$\sigma^2 = \\frac{1}{n}\sum{(x_i-\overline{x})^2}$   
$var(\overline{x}) = \\frac{\sigma^2}{n} *\\frac{N-n}{N-1}$   
$\sigma = \sqrt{var(\overline{x})}$'''
    return pc.copy(s)
def fin_pok():
    s = '''$\\alpha = ...$,$k=3$   
$ d^2 = \\frac{1}{n}\sum{(\overline{x_j}-\overline{x})^2n_j}$   
$ \overline{\sigma^2} = \\frac{1}{n}\sum{\sigma^2_jn_j}$   
$sse = n* \overline{\sigma^2}$   
$mse = \\frac{sse}{n-k}$   
$ sstr = n* d^2$   
$mstr = frac{sstr}{k-1}$    
$F = \\frac{mstr}{mse}$   
$k_\\alpha = f(k-1,n-k).isf(\\alpha)$      
$pv = f(k-1,n-k).sf(F)$'''
    return pc.copy(s)
def fin_pok_file():
    s = '''$\\alpha = ...$,   
$k=3$    
$ \delta^2 = \\frac{1}{n}\sum{(\overline{x_j}-\overline{x})^2n_j}$    
$ \overline{\sigma^2} = \\frac{1}{n}\sum{\sigma^2_jn_j}$   
$sse = n* \overline{\sigma^2}$   
$MSE = \dfrac{SSE}{n - k}$   
$SSTR = n * \delta^2$   
$MSTR = \dfrac{SSTR}{k-1}$   
$F = \dfrac{MSTR}{MSE}$   
$k_{\\alpha} = f(k-1, n-k).isf(\\alpha)$   
$pv = f(k-1, n-k).sf(\\alpha)$   
$\Theta_{1,2} = \overline{A} ± t.(N-k).isf(\dfrac{1-0.91}{2}) * \sqrt{\dfrac{MSE}{h_a}}$'''
    return pc.copy(s)
def f_f():
    s ='''$\overline{x}=\\frac{1}{n}\sum{x_i}$   
$\sigma = \sqrt{\\frac{1}{n}\sum{(x_i-\overline{x})^2}}$   
$z$ ~ $N(0,1)$   
$L = z.ppf(0.25)$
$H = z.isf(0.25)$   
$ N = \sum{I_{[L<=x<=H]}}$   
расстояние между $\hat{F}$ и F
$\hat{F}$ ~ выюорочная ф-ия распределения
$d = sup|F.cdf(x)-N.cdf(x)|$'''
    return pc.copy(s)
def raspr_ballov():
    s = '''$N = sum([\\text{число работ}])$   
$n = \\frac{N}{\\text{число преподователей}}$  
$E(\overline {x}) =E(x)=\\frac{1}{n} \sum{X_k n_k} $   
$\sigma(\overline{x}) = \\frac {\sigma^2} {n} \\frac {N-n} {N-1} $'''
    return pc.copy(s)

def moneta():
    s = '''и подставь цифры

$I$   $[1,0]$   
$R(*) [\dfrac{1}{2}, \dfrac{1}{2}]$   
$E(I) = \dfrac{1}{2}$   
$Var(I) = \dfrac{1}{2} - \dfrac{1}{4} = \dfrac{1}{4}$   
$E(\overline{X} - ?)$   
$Var(\overline{X} -?)$   
$X_i = \sum_{i=1}^{11}I_i, \overrightarrow{X} =$ {$x_1,x_2,\cdots,x_{N}$}$\overline{X} = \dfrac{\sum_{i=1}^{N}X_i}{n}; $   
N = 257, причем {$I_{i1}, I_{i2}, \cdots, I_{i11}$} $\\ne$ {$I_{j1}, I_{j2}, \cdots, I_{j11}$}   
По теореме $E(\overline X) = E(X) = E(\sum_{i=1}^{11}I_i) = \sum_{i=1}^{11} E(I_i) = \dfrac{1}{2} * 11 = 5,5$   
Выборка безвозвратная, значит   
$Var(\overline X) = \dfrac{Var(X)}{n} * \dfrac{N-n}{N-1}$   
$Var(X) = Var(\sum_{i=1}^{11}I_i) = \sum_{i=1}^{11}Var(X_i) = 11Var(X) = \dfrac{11}{4}$   
N = |$\Omega$| = $2^{k}$ = 2048'''
    return pc.copy(s)

def lnl():
    s = '''$ f(x,y) = \\frac{1} {2\pi \sigma^2 \sqrt{1-\\rho^2}} e -$
$\\frac{(x-\mu_x)^2-2\\rho (x- \mu_x)(y-\mu_y)+ (y-\mu_y)^2} {2 \sigma^2 (1- \\rho)^2} $   
$L (x, y, \hat {\sigma} , \hat {\\rho}) = \prod f (x, y) $   
$ \ln L = -\ln (2\pi) -\\frac {1}{2} \ln (1-\\rho^2)-\ln\sigma^2- \\frac{1}{2(1-\\rho^2)} \\frac {\sum{(x-\mu_x)^2}-2\\rho(x-\mu_x)(y-\mu_y)+(y-\mu_y)^2}{n\sigma^2}  $
  
{$\\frac{d\ln L} {d\sigma} =0$__  $\hat{\\rho}=... $  
{$ \\frac {d\ln L} {d\\rho} =0$ ___ $\hat{\sigma}=...$'''
    return pc.copy(s)

def zpawxy():
    s = '''$\sigma_x =\sqrt{ N(\mu_x, ...^2)[1]}$, $d = \mu_x-\mu_y$   
$n = i(x_i), m = i(y_i)$   
$\sigma_y = \sqrt{N(\mu_y,...^2)[1]}$   
$\\alpha = ...$    
$ z = \\frac{\overline {X} - \overline {Y}}{\sqrt {\sigma_x^2 *n + \sigma_y^2 * m}} $   
$K_\\alpha : (Z_\\alpha ; \infty) $  
$Z_\\alpha -\\text {процентная точка } $$ Z $ ~ $ N (0, 1) $  
$ \text {так как} K_\\alpha - \\text{ правосторон., то} $   
$ P= pv (\\vec{z}) = P (Z_\\text{ распр} \geq {z}_\\text{стат})= Z_0 sf (z) $   
$A =Z_\\alpha = Z. isf(\\alpha)  $  
$w =\\frac{1} {2} - \Phi _0 (z_\\alpha - $
$\\frac {\sqrt{nm}}{\sqrt {\sigma_x^2 m + \sigma_y^2 n}} d )  $'''
    return pc.copy(s)

def tapw():
    s = '''$\mu_0 = H_0 \mu$ ___ $\mu_1 = H_1 \mu$   
$\\alpha =...$___ $n = ...$   
$ t = \\frac {\sqrt {n} (\overline{x} - \mu_0)} {S}$ _
$S^2= \\frac {1} {n-1} \sum^n ({x_i - \overline {x}) ^2} $  
$A = t (n-1) . ist (\\frac {\\alpha} {2} )  $  
$T = t (n-1) $  
$P =2 min (T.cdf(t) , T.sf(t))  $   
$ w- \\text{на питоне} $'''
    return pc.copy(s)

def tabl_chast_ex_var():
    s = '''$ E (\overline{x}) = E (x) = \overline{x} = \\frac{1}{n} \sum{x_k} $   
$ Var (\overline{y}) = \\frac{sigma_y^2}{n} \\frac{N-n}{N-1} $   
$ Var (\overline{x}) =\\frac{sigma_x^2}{n} \\frac{N-n}{N-1}  $    
$ \sigma \overline{y} =\sqrt{{Var (\overline{y})}} \\ $
$ \sigma \overline{x} = \sqrt{ Var({ \overline{x})}} $   
$ cov (x ; y) = \overline{xy}- \overline{x} *\overline{y}\\  $
$ \hat{cov} (\overline {x} ; \overline {y}) = \\frac{cov (x,y)} {n} \\frac {N-n} {N-1}  $   
$ \\rho = \\frac {\hat {cov} ( \overline {x}, \overline {y} )} {\hat {\sigma}_{\overline {x}} {\hat {\sigma} _ {\overline {y}}}}\\ $'''
    return pc.copy(s)


def ro_theta():
    s = '''$\\alpha = 1-...$   
$cov(x,y) = np.cov(x,y)$   
$ \hat{\\rho} = \\frac{\hat{cov(x,y)}}{\hat{\sigma_x} \hat{\sigma_y}}\\$ 
$ \hat{\\theta_2} = tanh(arth(\hat{\\rho})+\\frac{1}{\sqrt{n-3}}Z.isf(\\frac{\\alpha}{2})) $'''
    return pc.copy(s)

def xi():
    s = '''$H_0: \sigma = ...$   
$H_1: \sigma \\ne ...$   
$alpha = ...$   
критерий $\chi^2_{набл}$, крит обл. - двухсторон.   
$\chi^2$ набл = $\\frac{s^2}{\sigma^2}= \\frac {(n-1)s^2} {\sigma^2}$ , $S \\text{ испр.дисперсия} $   
$ \chi^2_{окр} = (\chi^2 $ набл $ < \chi^2 _{1-\\frac {\\alpha} {2}}$ $(n-1)) \cup (\chi^2 $ набл $ \supset \chi^2_\\frac {\\alpha} {2}$
$(n-1))= (-\infty ; a) \cup (b; +\infty)  $  
$ \\text {Если} \chi^2 $ набл $ \in \chi^2_\\text{окр} , \\text {Но  отверг , иначе Ho не отверг }   $  
$ A =ip (\chi^2 $ набл $ < \chi^2_{1-\\frac {\\alpha} {2}} (n-1))= \chi^2(n-1). cdf (1 - \\frac {\\alpha} {2})= ... $  
$ B =ip (\chi^2 $ набл $ > \chi^2 _ \\frac{\\alpha} {2} (n-1))= \chi^2 (n-1) sf`(\\frac{\\alpha}{2}) = ...  $  
$ \\beta =ip (\\frac {\sigma^2} {\sigma^2_1}B < \chi^2(n-1))-ip(\\frac{\sigma^2} {\sigma^2_1} A > \chi^2 (n-1))= ... $'''
    return pc.copy(s)
def xi0():
    s = '''$H_0: \sigma = ...$    
$H_1: \sigma \ne ...$   
$alpha = ...$   
$\chi^2_{0набл}$, крит обл. - двухсторон.   
$\chi^2_{0набл}$ = $\dfrac{\dfrac{s}{\sigma^2}}{n} = \dfrac{n*s^2_0}{\sigma^2_0} = \sum_{i=1}^n(x_i - \mu)^2*\dfrac{1}{\sigma^2_0}$   
$\chi^2_{окр} = (\chi_{0набл}^2 <\chi_0^2\dfrac{(n)}{1-\dfrac{\\alpha}{2}}) \cup (\chi_{0набл}^2 >\chi^2\dfrac{(n)}{\dfrac{\\alpha}{2}}) = (-∞; a) \cup (\sigma_i; ∞)$   
Если $\chi^2_{0набл} \in \chi^2_{окр},H_о$ отверг., иначе $H_o$ не отверг.   
A = IP $(\chi_{0набл}^2 <\chi_0^2\dfrac{(n)}{1-\dfrac{\\alpha}{2}}) = \chi^2(n).cdf(1-\dfrac{1}{\\alpha}$) = ...     
B = IP $(\chi_{0набл}^2 >\chi^2\dfrac{(n)}{\dfrac{\\alpha}{2}}) = \chi^2(n).sf(1-\dfrac{1}{\\alpha}$) = ...    
$\\beta = IP(\dfrac{\sigma^2_0}{\sigma^2_1}*B < \chi^2(n)) - IP(\dfrac{\sigma^2_0}{\sigma^2_1}*A > \chi^2(n))$ = ...'''
    return pc.copy(s)
