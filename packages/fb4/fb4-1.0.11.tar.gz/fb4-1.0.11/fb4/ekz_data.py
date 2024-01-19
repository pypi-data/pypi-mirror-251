from dataclasses import dataclass


@dataclass
class Tasks:
    data = {
        "Q1": {
            1:
                (r'''Дайте определение случайной величины, которая имеет гамма-распределение $Γ(\alpha, \lambda)$, и выведите основные свойства гамма-расределения. Запишите формулы для математичсекого ожидания E(X) и дисперсии Var(X) гамма-распределения.''',
                 r'''Случайная величина $X$ имеет **гамма-распределение** $\left(X \sim \Gamma(\alpha, \lambda)\right)$, если плотность распределения задаётся как:

$\color{orange}{f_{\alpha, \lambda}(x) =
\begin{cases}
\frac{\alpha^\lambda}{\Gamma(\lambda)}\cdot e^{-\alpha x} \cdot x^{\lambda - 1},\ x > 0\\
0,\ x \leq 0
\end{cases}}$

где $\alpha > 0$ - параметр масштаба и $\lambda > 0$ - параметр формы.

<br>

**Свойства**

1. Если $X$ и $Y$ - независимые СВ, $X \sim \Gamma(\alpha, \lambda_1),\ Y \sim \Gamma(\alpha, \lambda_2)$, то
$\color{orange}{(X + Y) \sim \Gamma(\alpha, \lambda_1 + \lambda_2)}$

2. Если $X \sim \Gamma(\alpha, \lambda),\ k > 0$ - некоторая константа, то $\color{orange}{kX \sim \Gamma(\alpha, k\lambda)}$

3. Если $X = Z^2$, где $Z \sim N(0, 1)$, то $\color{orange}{X \sim \Gamma\left(\frac12, \frac12\right)}$

4. Если $\lambda = 1$, то $\Gamma(\alpha, 1) = Exp(\alpha)$
<br>
Действительное, если $\lambda = 1$, то плотность имеет вид:
<br>
$f_{\alpha, 1}(x) =
\begin{cases}
\alpha\cdot e^{-\alpha x},\ x > 0\\
0,\ x \leq 0
\end{cases}$
<br>
что соответствует плотности распределения экспоненциального закона.

<br>

**Математическое ожидание и дисперсия**

Если $X \sim \Gamma(\alpha, \lambda)$, то:

$\color{orange}{E(X) = \frac\lambda\alpha}$

$\color{orange}{Var(X) = \frac{\lambda}{\alpha^2}}$

**Вывод**

$E(X) = \int_0^{+\infty} \frac{x\alpha^\lambda x^{\lambda-1}e^{-\alpha x}}{\Gamma(\lambda)}dx \stackrel{\color{lightgreen}{t = \alpha x,\ dt = \alpha dx}}{=}
\frac1{\alpha\Gamma(\lambda)} \int_0^{+\infty} e^{-t}t^\lambda dt \stackrel{\color{lightgreen}{опр.\ \Gamma}}{=}
\frac{\Gamma(\lambda + 1)}{\alpha \Gamma(\lambda)} \stackrel{\color{lightgreen}{\Gamma(k + 1) = k\Gamma(k)}}{=}
\frac{\lambda \Gamma(\lambda)}{\alpha \Gamma(\lambda)} = \frac\lambda\alpha$

$Var(X) = \int_0^{+\infty} \frac{x^2\alpha^\lambda x^{\lambda-1}e^{-\alpha x}}{\Gamma(\lambda)}dx - E^2(X) \stackrel{\color{lightgreen}{t = \alpha x,\ dt = \alpha dx}}{=}
\frac1{\alpha^2\Gamma(\lambda)} \int_0^{+\infty} e^{-t}t^{\lambda + 1} dt - E^2(X) \stackrel{\color{lightgreen}{опр.\ \Gamma}}{=}
\frac{\Gamma(\lambda + 2)}{\alpha^2 \Gamma(\lambda)} - E^2(X) \stackrel{\color{lightgreen}{\Gamma(k + 1) = k\Gamma(k)}}{=}
\frac{\lambda (\lambda + 1) \Gamma(\lambda)}{\alpha^2 \Gamma(\lambda)} - \frac{\lambda^2}{\alpha^2} = \frac{\lambda^2 + \lambda - \lambda^2}{\alpha^2} = \frac{\lambda}{\alpha^2}$

<hr>'''),
            2:
                (r'''Дайте определение случайной величины, которая имеет $\chi^2$-распределение с $n$ степенями свободы. Запишите плотность $\chi^2$-распределения. Выведите формулы для математического ожидания $\mathbb{E}(X)$ и дисперсии $Var(X)$ $\chi^2$-распределения с $n$ степенями свободы.


1) Найдите $\mathbb{P}(\chi_{20}^2 > 10.9)$ , где $\chi_{20}^2$ – случайная величина, которая имеет $\chi^2$–распределение с 20 степенями свободы;
2) Найдите 93% (верхнюю) точку $\chi_{0.93}^2(5)$ хи-квадрат распределения с 5 степенями свободы.''',
                 r'''$\mathbb{P}(\chi_{20}^2 > 10.9) = 0.948775, \quad \chi_{0.93}^2(5) = 1.34721$

Пусть $Z_1, ..., Z_n$ - независимые, одинаково распределенные случайные величины, имеющие стандартное нормальное распределение, $Z_k \sim N(0;1)$. Распределение случайной величины $$\mathcal{X}_n^2 = Z_1^2 + ... + Z_n^2$$ называется распределением $\mathcal{X}^2(n)$ ("хи-квадрат") c n степенями свободы. (Обозначение: $\mathcal{X}_n^2 \sim \mathcal{X}^2(n)$.
<br>
Плотность распределения имеет вид: $$ f_{\mathcal{X}_n^2}(x) = \begin{cases}
\frac{1}{\Gamma(\frac{n}{2})2^{\frac{n}{2}}} \cdot x^{\frac{n}{2}-1} e^{-\frac{x}{2}}, x>0\\
0, \text{ иначе}
\end{cases}$$
<br>
Выведем формулы для математического ожидания и дисперсии:
$Z_k \sim N(0;1). \text{ Тогда } X_k = Z_k^2 \sim \Gamma(\frac{1}{2};\frac{1}{2})$
<br>
Далее, $\mathcal{X}^2 = Z_1^2 + Z_2^2 + ... + Z_n^2 = X_1 + X_2 + ...+ X_n \sim \Gamma(\frac{1}{2},\frac{1}{2}+...+\frac{1}{2}) = \Gamma(\frac{1}{2};\frac{n}{2})$
<br>
$\mathbb{E}(\mathcal{X}_n^2) = \frac \lambda a = \frac{n}{2} \div \frac{1}{2} = n \\ Var(\mathcal{X}_n^2) = \frac{\lambda}{a^2} = \frac{n}{2} \div \frac{1}{4} = 2n$

<hr>
```
chi2(20).sf(10.9), chi2(5).isf(0.93)
```
'''),
            3:
                (r'''Дайте определение случайной величины, которая имеет распределение Стьюдента с n степенями свободы Как связаны распределение Коши и распределение Стьюдента? Запишите плотность рас-
пределения Стьюдента с четырьмя степенями свободы. Найдите а) P(−2.5 6 t5 < −1.7), где $t_5$ – случайная величина, которая имеет распределение Стьюдента с 5 степенями свободы; б) найдите
10% (верхнюю) точку $t_{0.1}$(7) распределения Стьюдента 7 степенями свободы.
Ответ: $а) P(−2.5 \leq t_5 < −1.7) = 0.0476933; t_{0.1}(7) = 1.41492.$''',
                 r'''Пусть $Z, X_1, X_2, ..., X_n$ - независимые одинаково распределенные случайные величины, причем $Z, X_k, \sim N(0;1), k = 1, ...,n$ и пусть $\mathcal{X}_n^2 = \displaystyle\sum_{i=1}^{n}X_n^2 \sim \mathcal{X}^2(n)$. Распределение случайной величины $$t_n = \frac{Z}{\sqrt{\frac{\mathcal{X}_n^2}{n}}} = \frac{Z}{\sqrt{\frac{1}{n}\displaystyle\sum_{i=1}^{n}X_k^2}}$$ называется распределением Стьюдента с n степенями свободы.
<br>
Плотность распределение:
$$ f_{t,n}(x) = B_n(1 + \frac{x^2}{n})^{-\frac{n+1}{2}} , x \in \mathcal{R}^2$$,
<br>
где нормирующий множитель $B_n = \frac{\Gamma(\frac{n+1}{2})}{\sqrt{\pi n}\Gamma(\frac{n}{2})}$
<br>
Co(0;1) и t(1) имеют аналогичные плотности:
<br>
$Co(0;1) = \frac{1}{\pi} (\frac{1}{x^2 + 1})$
<br>
$t(1) = \frac{\Gamma(\frac{1+1}{2})}{\sqrt{\pi}\Gamma(\frac{1}{2})} \cdot (1 + \frac{x^2}{1})^{-\frac{1+1}{2}} = \frac{1}{\pi} (x^2 + 1)^{-1}$

<br>

**Пример**

Плотность распределения с 4 степенями свободы:
<br>
$B_4 = \frac{\Gamma(\frac{4+1}{2})}{\sqrt{4\pi}\Gamma(\frac{4}{2})} = \frac{\frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi}}{2\sqrt{\pi}\cdot1!} = \frac{3}{8}$
<br>
$f_4(x) = B_4 (1 + \frac{x^2}{4})^{-\frac{(4+1)}{2}} = \frac{3}{8} \cdot (1 + \frac{x^2}{4})^{-2.5}$

<hr>
```
t(5).cdf(-1.7) - t(5).cdf(-2.5), t(7).isf(0.1)
```
'''),
            4:
                (r'''Дайте определение случайной величины, которая имеет распределение Фишера F(n, m) с n и m

степенями свободы. Запишите плотность распределения Фишера F(n, m) с n и m степенями свободы. Какой закон распределения имеет случайная величина $\frac{1}{F}$ , если случайная величина F имеет

распределение Фишера F(n, m) с n и m степенями свободы? Ответ необходимо обосновать. Найди-
те $а) P(3.1 \leq \frac{1}{F} < 10.7)$, где F – случайная величина, которая имеет распределение Фишера с 3 и 5
степенями свободы, F $\sim$ F(3; 5); б) найдите 5% (верхнюю) точку $F_{0.05}$(13; 4) распределения Фишера
с 13 и 4 степенями свободы.''',
                 r'''Пусть $X \sim \mathcal{X}^2(n), Y \sim \mathcal{X}^2(m)$ - независимые случайные величины, каждая из которых имеет "хи-квадрат" распределение с n и m степенями свободы соответсвенно. Распределение случайной величины $$\mathbb{F} = \frac{X/n}{Y/m} = \frac{m}{n} \cdot \frac{X}{Y}$$ называется распределением Фишера-Снедекера с числом степеней свободы n и m.
<br>
Плотность распределения: $$f_{\mathbb{F}}(x) =
\begin{cases}
\frac{\Gamma(\frac{m+n}{2})m^{\frac{m}{2}}n^{\frac{n}{2}}}{\Gamma(\frac{m}{2})\Gamma(\frac{n}{2})} \cdot \frac{x^{\frac{n}{2}-1}}{(m+nx)^{\frac{m+n}{2}}}, x>0\\
0, x \leq 0\\
\end{cases}$$

<br>

Распределение $\frac{1}{F}$:
<br>
$F \sim F(n,m), F = \frac{X/n}{Y/m} = \frac{m}{n} \cdot \frac{X}{Y}, \text{где } X \sim \mathcal{X}^2(n), Y \sim {X}^2(m)$ - независимые случайные величины
<br>
$F(\frac{1}{\mathcal{F}}) = P(\frac{1}{\mathcal{F}}<x) = P(\frac{1}{\frac{X/n}{Y/m}}<x)
= P(\frac{1}{\frac{X \cdot m}{Y \cdot n}}<x)
= P(\frac{n}{m} \cdot \frac{Y}{X}<x) \Longrightarrow \frac{1}{F} \sim F(m,n)$

<hr>
```
# F = f(n, m), 1/F = f(m, n)

f(5, 3).cdf(10.7) - f(5, 3).cdf(3.1), f(13, 4).isf(0.05)
```
'''),
            5:
                (r'''Дайте определения процентной точки и квантили. Укажите связь между процентными точками и квантилями. Сформулируте основные свойтсва процентных точек. Выведите формулу для нахож-
дения процентной точки стандартного нормального закона распределения через функцию Лапла-
са $\Phi_0(x)$. Найдите P(0.3 < $Z^2$ < 3.7), если случайная величина Z имеет стандартное нормальное

распределение, Z $\sim$ N(0; 1).''',
                 r'''**Квантилем** или левосторонней критической границей называется решение уравнения $F(x) = q$, где $F(x) = P(X \leq x)$ - функция распределения.
<br>
Квантиль уровня $q = 1 - a$ называется 100a% **процентной точкой** и обозначается $x_a$ (или называется правосторонней критической границей или верхней процентной точкой). $P(X>x_a) = a$

<br>

**Связь процентной точки и квантиля**
<br>
$q = 1 - a$

<br>

**Свойства процентных точек**

1. $z_{1-a} = -z_a$, где $z_a$  процентная точка нормального распределения $N(0;1)$
2. $t_{1-a}(k) = -t_a(k)$, где $t_a(k)$ процентная точка распределения Стьюдента t(k)
3. $F_{1-a}(k,l) = \frac{1}{F_a(k,l)}$ , где $F_a(k,l)$ процентная точка распределения Фишера F(n,m)
4. $t_a(k) \approx z_a, k>30$
5. $\mathcal{X}_a^2(k) = \frac{1}{2}(z_a + \sqrt{2k-1})^2, k>30$

<br>

**Формула нахождения процентной точки нормального закона через функцию Лапласа**

$P(Z>z_a) = 1 - P(Z \leq z_a) = 1 - F(z_a) = 1 - (Ф(z_a) + \frac{1}{2}) = \frac{1}{2} - Ф(z_a) = a \\ Ф(z_a) = \frac{1}{2} - a\\ z_a = Ф(\frac{1}{2} - a)^{-1}$

Для доказательства 1 и 2 свойства нужно учесть то, что стандартное нормальное распределение и распределение симметричны, а их математические ожидания равны нулю.
<br>
Рассмотрим, к примеру, нормальное стандартное распределение. $z_{1-a} = Z(a)$. $Z(a)$ и $z_a$ отмеряют одинаковые "хвосты" распределения слева и справо соответственно. (так как распределение симметрично) Так как слева стоят числа меньшие 0, а справа большие, то полученные величины будут противоположны по знаку.(так как математическое ожидание распределения = 0). В итоге получим: $z_{1-a} = -z_a$, где $z_a$. Аналогично для распределения Стьюдента.
<hr>
```
chi2(1).cdf(3.7) - chi2(1).cdf(0.3)
```
'''),
            6: (r'''Сформулируйте определение случайной выборки из конечной генеральной совокупности. Какие виды выборок вам известны? Перечислите (с указанием формул) основные характеристики выборочной и генеральной совокупностей.''',
                r'''Совокупность, из которой извлекаются элементы, называется генеральной, тогда как совокупность, образованная отобранными элементами, называется выборочной.

**Случайной выборкой из конечной генеральной совокупности** назывется результат множество наблюдений $x_1, ..., x_n$, где n - объем выборки, отобранной случайным образом из генеральной совокупности.

**Виды**

Выборка бывает повторной и бесповторной.

**Повторная выборка** - совокупность, образованная по следующей схеме: сначала из генеральной совокупности случайным равновероятным образом извлекается один элемент; затем этот элемент возвращается в генеральную совокупность и все повторяется, пока не будет отобрано необходимое число элементов.

**Бесповторная выборка** - совокупность, образованная по аналогичной схеме, но отобранные элементы в генеральную совокупность не возвращаются.

$\begin{array}{|l|c|c|}
\hline
{Характеристики \\ параметров \\распределения} & {генеральная \\ совокупность} & {выборочная \\совокупность}\\
\hline
\text{Объем выборки} & N & n\\
\hline
{\text{Численность единиц} \\ совокупности, обладающих \\ \text{признаком x}}& N_x & n_x\\
\hline
{\text{Доля единиц, обладающих}\\ \text{изучаемым признаком x}} & p = \frac{N_x}{N} & w = \frac{n_x}{n}\\
\hline
{Дисперсия} & \sigma^2 = p(1-p) & \sigma^2 = w(1-w)\\
\hline
\text{Среднее квадратичное отклонение} & \sigma = \sqrt{p(1-p)} & \sigma = \sqrt{w(1-w)}\\
\hline
\text{Среднее значение признака} & \mu = \frac{\sum x_i}{N} & \overline{x} = \frac{\sum x_i}{n}\\
\hline
{Дисперсия} & \sigma^2 = \frac{\sum(x_i - \mu)^2}{N} & s^2 = \frac{\sum(x_i-\overline{x})^2}{n}\\
\hline
\text{Среднее квадратичное отклонение} & \sigma = \sqrt{\frac{\sum(x_i - \mu)^2}{N}} & s = \sqrt{\frac{\sum(x_i-\overline{x})^2}{n}}\\
\hline
\end{array}$

<hr>'''),
            7: (r'''Сформулируйте определение случайной выборки из распределения. Как в этом случае определяются: выборочное среднее, начальные и центральные моменты выборки, функция распределения выборки? Что в данном контексте означает генеральное среднее?''',
                r'''**Случайной выборкой** объема n из распределения $\mathcal{L}$ называется последовательность n независимых случайных величин $X_1, X_2, ...X_n$, распределенных по одному и тому же закону $\mathcal{L}$. При этом n - объем случайной выборки, а случайные величины $X_1, X_2, ...X_n$ - элементы случайной выборки. Набор чисел $x_1, x_2, ... x_n$ - возможных значений $X_1, X_2, ...X_n$ называется реализацией случайной выборки.

<br>

**эмпирическое среднее**:
<br>
$\overline{x} = \frac{x_1 + ...+x_n}{n} = \frac{n_1x_1 + ...+n_sx_s}{n}$

**эмпирическая дисперсия**:
<br>
$ \hat{\sigma}^2 = \overline{(x-\overline{x})^2} =
\frac{1}{n}\sum\limits_{i=1}^n(x_i - \overline{x})^2
= \frac{1}{n}\sum\limits_{s=1}^k n_s(x_s - \overline{x})^2
= \overline{x^2} - (\overline{x})^2$

**эмпирические начальные моменты k-ого порядка**:
<br>
$\hat{v}_k = \overline{x^k} = \frac{1}{n}\displaystyle\sum_{i=1}^{n}x_i^k = \frac{1}{n}\displaystyle\sum_{i=1}^{n}n_ix_i^k$

**эмпирические центральные моменты k-ого порядка**:
<br>
$\hat{\mu}_k = \overline{(x-\overline{x})^k} = \frac{1}{n}\displaystyle\sum_{i=1}^{n}(x_i - \overline{x})^k$

**эмпирическая функция распределения**:
<br>
$\hat{F}_n(x) = \frac{\{\text{количество } x_i: x_i \leq x\}}{n} = \frac{1}{n} \sum\limits_{s:x_s \leq x} n_s$

<br>

**Генеральное среднее** - среднее арифметическое значение признака генеральной совокупности
<br>
1. Если значение признака различны, то
<br>
$x_r = \frac{1}{N}\displaystyle\sum_{i=1}^{N}x_i$
2. Если значения признака имеют частоты
<br>
$x_r = \frac{1}{N}\displaystyle\sum_{i=1}^{N}x_i N_i$

<hr>'''),
            8:
                (r'''Запишите формулы для математического ожидания и дисперсии выборочной доли в случае повторной (бесповторной) выборки. Поясните все используемые обозначения.''',
                 r'''**Повторной выборкой** называется совокупность образованная по следующей схеме:
<br>
сначала из генеральной совокупности случайным равновероятным образом извлекается один элемент;
<br>
затем этот элемент возвращается в генеральную совокупность и все повторяется нужное количество раз

**Бесповторной выборкой** называется совокупность образованная по аналогичной  схеме, но с одним отличием - отобранные элементы в генеральных совокупность не возвращаются.

<br>

Отношение $p_i = \frac{N_i}{N}$ (соответственно $\hat{p_i} = \frac{n_i}{n}$) называется **генеральной** (соответственно **выборочной**) **долей** значения $x_i$, признака X. Где N и n объёмы генеральной и выборочной совокупностей.

Пусть p - генеральная, а $\hat{p_i}$ - выборочная доля какого-либо значения x_i признака X, q = 1 - p
<br>
Тогда:

- При повторной выборке:
<br>
$E(\hat{p_i}) = p$
<br>
$Var(\hat{p_i}) = \frac{pq}{n}$
- При бесповторной выборке:
<br>
$E(\hat{p_i}) = p$
<br>
$Var(\hat{p_i}) = \frac{pq}{n} \frac{N - n}{N - 1}$

<hr>'''),
            9:
                (r'''Сформулируйте определение выборочной функции распределения и докажите ее сходимость по
вероятности к теоретической функции распределения. Выведите формулы для математического
ожидания и дисперсии выборочной функции распределния.''',
                 r'''Пусть $X_1, X_2, ..., X_n$ - выборка объёма n из некоторого распределения $\mathcal{L}$

Зададим следующую случайную величину:

$\mu_n(x) = \{\text{кол-во элементов выборки X, значения которых не больше x}\} = \sum_{k=1}^n I_{\{X_k \leq x\}}$

где

$I_{\{X_k \leq x\}} =
\begin{cases}
1, X_k \leq x\\
0, X_k > x\\
\end{cases}$

**Выборочной функцией распределения** случайной выборки $X_1, ..., X_n$ называется функция, которая для каждого $x\in\mathbb R ^ 1$ является случайной величиной:

$\hat F_n(x) = \frac{\mu_n(x)}{n} = \frac1n \sum_{k=1}^{n} I_{\{X_k \leq x\}}$

<br>

**Теорема о сходимости по вероятности**

Для любого фиксированного $x \in \mathbb R^1$ справедливо

$$\hat F_n(x) \overset{P}{\underset{n \rightarrow +\infty}{\longrightarrow}} F(x)$$

т.е. для $\forall\ \varepsilon > 0 \underset{n \rightarrow +\infty}{\lim} P(|\hat F_n(x) - F(x)| < \varepsilon) = 1$

**Доказательство**

Исходя из закона больших чисел, если $E(x_i) = \alpha$, то $\frac1n \sum x_i \underset{n \rightarrow +\infty}{\overset{P}{\longrightarrow}} \alpha$

Рассмотрим $I_{\{X_k \leq x\}}$: её математическое ожидание равно:

$E(I_{\{X_k \leq x\}}) = 1\cdot P(x_i \leq x) + 0 \cdot P(x_i > x) = P(x_i \leq x) = F(x)$

 Подставим в закон больших чисел, получим:

$\frac1n \sum x_i \underset{n \rightarrow +\infty}{\overset{P}{\longrightarrow}} \alpha$

$\frac1n \sum I_{\{X_k \leq x\}} \underset{n \rightarrow +\infty}{\overset{P}{\longrightarrow}} F(x)$

$\hat F_n(x) \underset{n \rightarrow +\infty}{\overset{P}{\longrightarrow}} F(x)$

что и требовалось показать.

<br>

**Математическое ожидание и дисперсия $\hat F_n(x)$**

Величина $I_{\{X_k \leq x\}}$ подчиняется закону Бернулли, а значит

$E(I_{\{X_k \leq x\}}) = p$, $Var(I_{\{X_k \leq x\}}) = pq$,

где $p = E(I_{\{X_k \leq x\}}) = 1\cdot P(x_i \leq x) + 0 \cdot P(x_i > x) = P(x_i \leq x) = F(x)$

Тогда:

$E\left(\hat F_n(x)\right) = E\left(\frac1n \sum_{k=1}^{n} I_{\{X_k \leq x\}}\right) = \frac1n E\left(\sum_{k=1}^{n} I_{\{X_k \leq x\}}\right) =  \frac{n \cdot E\left(I_{\{X_k \leq x\}}\right)}{n} = p = F(x)$

$Var\left(\hat F_n(x)\right) = Var\left(\frac1n \sum_{k=1}^{n} I_{\{X_k \leq x\}}\right) = \frac1{n^2} Var\left(\sum_{k=1}^{n} I_{\{X_k \leq x\}}\right) = \frac1{n^2} \sum_{k=1}^{n} Var(I_{\{X_k \leq x\}}) =  \frac{n \cdot Var\left(I_{\{X_k \leq x\}}\right)}{n^2} = \frac{npq}{n^2} = \frac{F(x) (1 - F(x))}{n}$

<hr>'''),
            10:
                (r'''Дайте определение k-ой порядковой статистики. Выведение формулы для функций распределений экстремальных статистик.''',
                 r'''Пусть $X_1, X_2, ..., X_n$ - выборка из некоторого распределения $\mathcal{L}$ и пусть $x_1, x_2, ..., x_n$ - произвольная её реализация.
Поставим в соответствие этой реализации упорядоченную последовательность
<br>
$x_{(1)} \leq x_{(2)} \leq ... \leq x_{(n)}$
<br>
в порядке возрастания так, что
<br>
$x_{(1)} = min(x_1, x_2, ..., x_n)$
<br>
$x_{(2)}$ - второе по величине значение
<br>
...
<br>
$x_{(k)}$ - k-ое по величине значение
<br>
...
<br>
$x_{(n)} = max(x_1, x_2, ..., x_n)$

Эта последовательность называется вариационным рядом, а её члены - порядковыми статистиками. Случайная величина $x_{(k)} = X_{(k)}$ называется **k-ой порядковой статистикой**.

<br>

**Вывод формулы для статистики $X_{(n)}$**

$F_{X_{(n)}}(x) \stackrel{\color{\lightgreen}{опр.}}{=} P(X_{(n)} \leq x) = P(X_1 \leq x,\ ...,\ X_n \leq x) \stackrel{\color{\lightgreen}{независ.}}{=} P(X_1 \leq x)\cdot\ ...\ \cdot P(X_n \leq x) \stackrel{\color{\lightgreen}{опр.}}{=} F(x) \cdot\ ...\ \cdot F(x) = F^n(x)$

<br>

**Вывод формулы для статистики $X_{(1)}$**

$F_{X_{(1)}}(x) \stackrel{\color{\lightgreen}{опр.}}{=} P(X_{(1)} \leq x) = 1 - P(X_{(1)} > x) = P(X_1 > x,\ ...,\ X_n > x) \stackrel{\color{\lightgreen}{независ.}}{=} 1 - P(X_1 > x)\cdot\ ...\ \cdot P(X_n > x) = 1 - (1 - P(X_1 \leq x))\cdot\ ...\ \cdot (1 - P(X_n \leq x)) \stackrel{\color{\lightgreen}{опр.}}{=} 1 - (1 - F(x)) \cdot\ ...\ \cdot (1 - F(x)) = 1 - (1 - F(x))^n$

<hr>'''),
            11:
                (r'''Что такое точечная статистическая оценка? Какие оценки называются несмещенными, состоятельными? Приведите пример оценки с минимальной дисперсией.''',
                 r'''Пусть $X_1, X_2, ..., X_n - $ выборка объёма n из перематрического распределения $ \mathcal{L}_{\theta}(X). $ Произвольная (вычислимая по выборочным данным) функция $ \hat{\theta}_n = T(X_1, X_2, ..., X_n)$ называется статистикой.

Пусть $\theta$ - параметр или иная характеристика генерального распределения $ \mathcal{L}_{\theta}(X)$. Статистика $ \hat{\theta} = \hat{\theta}_n = T(X_1, X_2, ..., X_n)$, которая предназначена для "приближённого" вычисления неизвестного параметра $\theta$, называется **точечной статистической оценкой** параметра $\theta$.

Статистическая оценка $ \hat{\theta} = \hat{\theta}_n = T(X_1, X_2, ..., X_n)$ неизвестного параметра $\theta$ называется **несмещённой** в среднем или просто несмещённой если:
<br>
$\color{orange}{E_{\theta}(\hat{\theta}) = \theta}$ для $\forall \theta \in \Theta$

Статистическая оценка $ \hat{\theta} = \hat{\theta}_n = T(X_1, X_2, ..., X_n)$ называется **состоятельной** если:
<br>
$\color{orange}{\lim\limits_{n\to +\infty}P(|\hat{\theta}_n - \theta| > \epsilon) = 0}$
или $\color{orange}{\hat{\theta}_n \xrightarrow[n \to +\infty]{P} \theta}$ для $\forall \theta \in \Theta$

<br>

**Пример**

Эффективные оценки:

1. $\hat \lambda = \overline X$ в законе Пуассона
2. $\hat \mu = \overline X$ в нормальном законе
3. $\hat p = \overline X$ в законе Бернулли $Bin(1, p)$
4. $\hat p = \frac{\overline X}{m}$ в законе Бернулли $Bin(m, p)$

**Доказательство эффективной оценки** (см. 16, 18, 19, 20)

Оценка с минимальной дисперсией это эффективная оценка. Найдём её с помощью неравенства Рао-Крамера
Пусть $X \sim Bin(m, \theta), \theta = p$. По определению информации Фишера $I(\theta) = \mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] \Longrightarrow$
<br>
1. $f(x,\theta) = P(X=x) = \theta^x(1 - \theta)^{1 - x}$;
<br>
2. $lnf(X,\theta) = Xln\theta + (1 - X)ln(1 - \theta)$;
<br>
3. $\frac{dlnf(X,\theta)}{d\theta} = \frac{X}{\theta} - \frac{1 - X}{1 - \theta} = \frac{X-\theta}{\theta(1 - \theta)}$;
<br>
4. $\mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] = \mathbb{E}\left[\frac{(X-\theta)^2}{\theta^2(1 - \theta)^2}\right] = \frac{1}{\theta^2(1 - \theta)^2}Var(X) = \frac{1}{\theta^2(1 - \theta)^2} \cdot m\theta(1 - \theta) = \frac{m}{\theta(1 - \theta)}$;
<br>
$I(\theta) = \frac{m}{\theta(1 - \theta)}$.

Рассмотрим теперь неравенство Рао-Крамера:
<br>
$Var_\theta(\hat{\theta_m}) \geq \frac{1}{mI(\theta)} \Longrightarrow Var_\theta(\hat{\theta_m}) \geq \frac{\theta(1 - \theta)}{m^2}$
<br>
Тогда если в качестве оценки взять $\hat{\theta_m} = \frac{\overline{X}}{m} \Longrightarrow Var_\theta(\hat{\theta_m}) = Var_\theta(\frac{\overline{X}}{m}) = \frac{Var(X)}{m^3} = \frac{\theta(1 - \theta)}{m^2}$
<br>
То есть для данной оценки неравенство превращается в равенство, следовательно оценка $\hat{\theta_n} = \frac{\overline{X}}{m}$ является эффективной оценкой, а значит имеет наименьшую дисперсию.

<hr>'''),
            12:
                (r'''Сформулируйте и докажите достаточное условие состоятельности оценки.''',
                 r'''**Теорема**

Если
- $E_\theta(\hat\theta_n) \underset{n \rightarrow +\infty}{\longrightarrow} \theta$ (т.е. оценка асимптотически несмещённая)
- $Var_\theta(\hat\theta_n) \underset{n \rightarrow +\infty}{\longrightarrow} 0$

то оценка $\hat \theta_n$ является состоятельной оценкой параметра $\theta$

<br>

**Доказательство**

Нам нужно показать состоятельность по определению:
$lim(P(|\hat\theta - \theta| < \varepsilon) = 1$

Исходя из неравенства Чебышева:
$\forall\varepsilon > 0: P(|\hat\theta - \theta|\geq \varepsilon) \leq \frac{Var(\hat\theta)}{\varepsilon^2}$

По условию известно, что $lim(Var(\hat \theta)) = 0$. Тогда, если взять предел обеих частей, то с одной стороны, известно, что $P(...) \geq 0$, с другой, по полученному неравенству $P(...) \leq lim(\frac{Var(\hat\theta)}{\varepsilon^2}) = 0$, то есть:

$\forall \varepsilon > 0: lim(P(|\hat \theta - \theta| \geq \varepsilon)) \rightarrow 0$

Меняя знак на противоположный, получаем, что:
$\forall \varepsilon > 0: lim(P(|\hat \theta - \theta| \leq \varepsilon)) \rightarrow 1 - 0 = 1$, что является состоятельностью по определению, чтд.

<hr>'''),
            13:
                (r'''Сформулируйте определение среднеквадратичной ошибки оценки. Какая оценка называется оптимальной? В чем заключается среднеквадратический подход к сравнению оценок?''',
                 r'''Определим **среднеквадратичную ошибку оценки** MSE:

$\color{orange}{\Delta = MSE = E_\theta\left[\left(\hat\theta_n - \theta \right)^2\right]}$

<br>

**Оптимальная оценка**

Пусть $\hat{\theta^*}$ и $\hat\theta$ - две несмещённые оценки параметра $\theta$.

Если $\color{orange}{\forall\ \theta, \hat\theta}$:

$\color{orange}{Var_\theta(\hat{\theta^*}) \leq Var_\theta(\hat\theta)}$,

то оценка $\hat{\theta^*}$ называется оптимальной

<br>

**Среднеквадратичный подход к сравнению оценок**

Оценка $\hat\theta_1$ "предпочтительнее" оценки $\hat\theta_2$ в смысле MSE, если:

$\color{orange}{MSE_1 \leq MSE_2}$

<hr>'''),
            14:
                (r'''Сформулируйте критерий оптимальности оценки, основанной на неравенстве Рао-Крамера.''',
                 r'''**Информационное неравенство Рао-Крамера**

Пусть $\hat\theta_n$ - несмещённая оценка в параметрической модели $\mathcal L_\theta(X)$, для которой выполнены условия регулярности. Тогда справедливо информационное неравенство Рао-Крамера:

$\large \color{orange}{Var_\theta(\hat\theta_n) \geq \frac{1}{n\cdot I(\theta)}}$

<br>

**Эффективная оценка по Рао-Крамеру**

Несмещенная оценка $\hat{\theta}$, для которой $\color{orange}{\forall{\theta} \in \Theta : Var_{\theta}(\hat{\theta_n}) = \frac{1}{nI(\theta)}}$, т.е. неравенство Рао-Крамера превращается в равенство для всех параметров $\theta$, называется эффективной оценкой по Рао-Крамера.

<hr>'''),
            15:
                (r'''Дайте определение информации по Фишеру и сформулируйте информационное неравенство Рао-
Крамера.''',
                 r'''**Информация по Фишеру**

Информацией по Фишеру для одного наблюдения $X$, которая представляет собой СВ, называется

$\color{orange}{\large I(\theta) = E_\theta\left[\left(\frac{\partial lnf(X, \theta)}{\partial\theta}\right)^2\right]}$,

где в выражении для плотности $f(x, \theta)$ заменили $x$ на $X$ (СВ).

<br>

**Информационное неравенство Рао-Крамера**

Пусть $\hat\theta_n$ - несмещённая оценка в параметрической модели $\mathcal L_\theta(X)$, для которой выполнены условия регулярности. Тогда справедливо информационное неравенство Рао-Крамера:

$\large \color{orange}{Var_\theta(\hat\theta_n) \geq \frac{1}{n\cdot I(\theta)}}$

<hr>'''),
            16:
                (r'''Сформулируйте определение эффективной оценки по Рао-Крамеру. Найдите эффективную оценку параметра $\theta$ для распределения Бернулли Bin(1, $\theta$).''',
                 r'''**Эффективная оценка по Рао-Крамеру**

Несмещенная оценка $\hat{\theta}$, для которой $\color{orange}{\forall{\theta} \in \Theta : Var_{\theta}(\hat{\theta_n}) = \frac{1}{nI(\theta)}}$, т.е. неравенство Рао-Крамера превращается в равенство для всех параметров $\theta$, называется эффективной оценкой по Рао-Крамера.

<br>

**Пример**

Пусть $X \sim Bin(1, \theta), \theta = p = 1\cdot p = np = E(X)$. По определению информации Фишера $I(\theta) = \mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] \Longrightarrow$
<br>
1. $f(x,\theta) = P(X=x) = \theta^x(1 - \theta)^{1 - x}$;
<br>
2. $lnf(X,\theta) = Xln\theta + (1 - X)ln(1 - \theta)$;
<br>
3. $\frac{dlnf(X,\theta)}{d\theta} = \frac{X}{\theta} - \frac{1 - X}{1 - \theta} = \frac{X-\theta}{\theta(1 - \theta)}$;
<br>
4. $\mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] = \mathbb{E}\left[\frac{(X-\theta)^2}{\theta^2(1 - \theta)^2}\right] = \frac{1}{\theta^2(1 - \theta)^2}Var(X) = \frac{1}{\theta^2(1 - \theta)^2} \cdot \theta(1 - \theta) = \frac{1}{\theta(1 - \theta)}$;
<br>
$I(\theta) = \frac{1}{\theta(1 - \theta)}$.

<br>

Рассмотрим теперь неравенство Рао-Крамера:
<br>
$Var_\theta(\hat{\theta_n}) \geq \frac{1}{nI(\theta)} \Longrightarrow Var_\theta(\hat{\theta_n}) \geq \frac{\theta(1 - \theta)}{n}$
<br>
Тогда если в качестве оценки взять $\hat{\theta_n} = \overline{X} \Longrightarrow Var_\theta(\hat{\theta_n}) = Var_\theta(\overline{X}) = \frac{Var(X)}{n} = \frac{\theta(1 - \theta)}{n}$
<br>
То есть для данной оценки неравенство превращается в равенство, следовательно оценка $\hat{\theta_n} = \overline{X}$ является эффективной оценкой.

<hr>
'''),
            17:
                (r'''Докажите несмещенность, состоятельность и эффективность (в классе всех линейных несмещенных оценок) выборочного среднего $\overline X$.''',
                 r'''Пусть $X_1, X_2, ..., X_n$ - выборка объема n из распределения $\mathcal{L}_\theta(X)$ и пусть $\theta = \mathbb{E}(X)$ и $\sigma^2 = Var(X)$ - параметры. Тогда выборочное среднее $\hat{\theta_n} = \overline{X}$ является несмещенной, состоятельной и эффективной в классе всех линейных несмещенных оценок параметр $\theta = \mathbb{E}(X)$
<br>
Докажем это:
<br>
$\mathbb{E}(\hat{\theta_n}) = \mathbb{E}(\overline{X}) = \frac{1}{n}(\mathbb{E}(X_1) + ... + \mathbb{E}(X_n)) = \frac{n}{n}\mathbb{E}(X) = \theta$ - несмещенная
<br>
$Var(\hat{\theta_n}) = Var(\overline{X}) = \frac{1}{n^2}(Var(X_1) + ... + Var(X_n)) = \frac{n}{n^2}Var(X) = \frac{\sigma^2}{n}\xrightarrow[n\to+\infty]{}0 $ - состоятельная
<br>
В классе линейных оценок любую оценку можно выразить, как $\hat{\theta_n} = \displaystyle\sum_{i=1}^{n} a_iX_i$. Из несмещенности следует, что $\displaystyle\sum_{i=1}^{n} a_i = 1$. Тогда $Var(\hat{\theta_n}) = Var(X) \displaystyle\sum_{i=1}^{n} a_i^2$. По определению оптимальности оценки $\hat{\theta_n^*} =\underset{\theta \in \Theta}{inf} Var(\hat{\theta_n})$, следовательно необходимо решать задачу оптимизации:
<br>
$\begin{cases}
Var(\hat{\theta_n}) \rightarrow \underset{a_i,i=\underline{1,i}}{min}\\
\displaystyle\sum_{i=1}^{n} a_i = 1 \\
\end{cases}$
<br>
Составим функцию Лагранжа:
<br>
$L =  \displaystyle\sum_{i=1}^{n} a_i^2 + \lambda( \displaystyle\sum_{i=1}^{n} a_i - 1)$.
<br>
Продиференцируем по переменным $a_i,\lambda$ и приравняем полученные выражения к нулю:
<br>
$\begin{cases}
\frac{dL}{da_i} = 0 \\
\frac{dL}{d\lambda} = 0 \\
\end{cases}\Longrightarrow
\begin{cases}
2a_i + \lambda = 0,\ i = \overline{1, n}\\
\displaystyle\sum_{i=1}^{n}a_i - 1 = 0 \\
\end{cases}\Longrightarrow
a_i = -\frac{\lambda}{2}$
<br>
Подставим $a_i$ во второе уравнение и получим: $\lambda = -\frac{2}{n}$. Подставим $\lambda$ обратно в $a_i$:
<br>
$a_i = \frac{1}{n}$. Отсюда $\hat{\theta_n^*} = \displaystyle\sum_{i=1}^{n} a_iX_i = \overline{X}$
<br>
То есть $\overline{X}$ - оптимальная оценка параметра $\theta = \mathbb{E}(X)$

<hr>'''),
            18:
                (r'''Сформулируйте определение эффективной оценки по Рао–Крамеру. Для распределения Пуассона
$\Pi(\lambda)$ предлагается оценка параметра $\lambda$: $\hat{\lambda}$ = $\overline X$. Покажите, что эта оценка является эффективной
по Рао-Крамеру.''',
                 r'''**Эффективная оценка по Рао-Крамеру**

Несмещенная оценка $\hat{\theta}$, для которой $\color{orange}{\forall{\theta} \in \Theta : Var_{\theta}(\hat{\theta_n}) = \frac{1}{nI(\theta)}}$, т.е. неравенство Рао-Крамера превращается в равенство для всех параметров $\theta$, называется эффективной оценкой по Рао-Крамера.

<br>

**Пример**

Пусть $X \sim П(\lambda), \lambda = \mathbb{E}(X) = Var(X)$. По определению информации Фишера $I(\lambda) = \mathbb{E}_\lambda[(\frac{dlnf(X,\lambda)}{d\lambda})^2] \Longrightarrow$
<br>
1. $f(X,\lambda) = P(X=k) = \frac{\lambda^k}{k!}e^{-\lambda}$;
<br>
2. $lnf(X,\lambda) = kln\lambda - lnk! - \lambda$;
<br>
3. $\frac{dlnf(X,\lambda)}{d\lambda} = \frac{k}{\lambda} - 1 = \frac{k-\lambda}{\lambda}$;
<br>
4.$\mathbb{E}_\lambda[(\frac{dlnf(X,\lambda)}{d\lambda})^2] = \mathbb{E}[\frac{(X-\lambda)^2}{\lambda^2}] = \frac{1}{\lambda^2}Var(X) = \frac{1}{\lambda}$;
<br>
$I(\lambda) = \frac{1}{\lambda}$.

<br>

Рассмотрим теперь неравенство Рао-Крамера:
<br>
$Var_\theta(\hat{\lambda_n}) \geq \frac{1}{nI(\lambda)} \Longrightarrow Var_\theta(\hat{\lambda_n}) \geq \frac{\lambda}{n}$
<br>
Тогда если в качесвте оценки взять $\hat{\lambda_n} = \overline{X} \Longrightarrow Var_\lambda(\hat{\lambda_n}) = Var_\lambda(\overline{X}) = \frac{Var(X)}{n} = \frac{\lambda}{n}$
<br>
То есть для данной оценки неравенство превращается в равенство, следовательно оценка $\hat{\lambda_n} = \overline{X}$ является эффективной оценкой.

<hr>'''),
            19:
                (r'''Сформулируйте информационное неравенство Рао–Крамера. Исследуйте на эффективность оценку $\hat p = \frac{\overline X}{m}$
для биномиального распределения Bin(m; p).''',
                 r'''**Информационное неравенство Рао-Крамера**

Пусть $\hat\theta_n$ - несмещённая оценка в параметрической модели $\mathcal L_\theta(X)$, для которой выполнены условия регулярности. Тогда справедливо информационное неравенство Рао-Крамера:

$\large \color{orange}{Var_\theta(\hat\theta_n) \geq \frac{1}{n\cdot I(\theta)}}$

<br>

**Пример**

Пусть $X \sim Bin(m, \theta), \theta = p$. По определению информации Фишера $I(\theta) = \mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] \Longrightarrow$
<br>
1. $f(x,\theta) = P(X=x) = \theta^x(1 - \theta)^{1 - x}$;
<br>
2. $lnf(X,\theta) = Xln\theta + (1 - X)ln(1 - \theta)$;
<br>
3. $\frac{dlnf(X,\theta)}{d\theta} = \frac{X}{\theta} - \frac{1 - X}{1 - \theta} = \frac{X-\theta}{\theta(1 - \theta)}$;
<br>
4. $\mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] = \mathbb{E}\left[\frac{(X-\theta)^2}{\theta^2(1 - \theta)^2}\right] = \frac{1}{\theta^2(1 - \theta)^2}Var(X) = \frac{1}{\theta^2(1 - \theta)^2} \cdot m\theta(1 - \theta) = \frac{m}{\theta(1 - \theta)}$;
<br>
$I(\theta) = \frac{m}{\theta(1 - \theta)}$.

<br>

Рассмотрим теперь неравенство Рао-Крамера:
<br>
$Var_\theta(\hat{\theta_m}) \geq \frac{1}{mI(\theta)} \Longrightarrow Var_\theta(\hat{\theta_m}) \geq \frac{\theta(1 - \theta)}{m^2}$
<br>
Тогда если в качестве оценки взять $\hat{\theta_m} = \frac{\overline{X}}{m} \Longrightarrow Var_\theta(\hat{\theta_m}) = Var_\theta(\frac{\overline{X}}{m}) = \frac{Var(X)}{m^3} = \frac{\theta(1 - \theta)}{m^2}$
<br>
То есть для данной оценки неравенство превращается в равенство, следовательно оценка $\hat{\theta_n} = \frac{\overline{X}}{m}$ является эффективной оценкой.

<hr>'''),
            20:
                (r'''Дайте определение информации по Фишеру. Вычислите информацию Фишера для нормального
закона распределения N($\mu; \sigma^2$
) (дисперсия $\sigma^2$ известна) и проверьте, что выборочное среднее $\overline X$ является эффективной оценкой параметра $\mu$ = E(X).''',
                 r'''**Информация по Фишеру**

Информацией по Фишеру для одного наблюдения $X$, которая представляет собой СВ, называется

$\color{orange}{\large I(\theta) = E_\theta\left[\left(\frac{\partial lnf(X, \theta)}{\partial\theta}\right)^2\right]}$,

где в выражении для плотности $f(x, \theta)$ заменили $x$ на $X$ (СВ).

<br>

**Пример**

Пусть $X \sim N(\theta, \sigma^2), \theta = \mu = E(X)$. По определению информации Фишера $I(\theta) = \mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] \Longrightarrow$
<br>
1. $f(x,\theta) = P(X=x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x - \theta)^2}{2\sigma^2}}$;
<br>
2. $lnf(X,\theta) = -ln(\sigma\sqrt{2\pi}) - \frac{(X - \theta)^2}{2\sigma^2}$;
<br>
3. $\frac{dlnf(X,\theta)}{d\theta} = \frac{X - \theta}{\sigma^2}$;
<br>
4. $\mathbb{E}_\theta\left[\left(\frac{dlnf(X,\theta)}{d\theta}\right)^2\right] = \mathbb{E}\left[\frac{(X - \theta)^2}{\sigma^4}\right] = \frac{1}{\sigma^4}Var(X) = \frac{1}{\sigma^2}$;
<br>
$I(\theta) = \frac{1}{\sigma^2}$.

<br>

Рассмотрим теперь неравенство Рао-Крамера:
<br>
$Var_\theta(\hat{\theta_n}) \geq \frac{1}{nI(\theta)} \Longrightarrow Var_\theta(\hat{\theta_n}) \geq \frac{\sigma^2}{n}$
<br>
Тогда если в качестве оценки взять $\hat{\theta_n} = \overline{X} \Longrightarrow Var_\theta(\hat{\theta_n}) = Var_\theta(\overline{X}) = \frac{Var(X)}{n} = \frac{\sigma^2}{n}$
<br>
То есть для данной оценки неравенство превращается в равенство, следовательно оценка $\hat{\theta_n} = \overline{X}$ является эффективной оценкой.

<hr>'''),
            21:
                (r'''Как производится оценка параметров абсолютно непрерывного распределения методом максимального правдоподобия? Какой вероятностный смысл в этом случае имеет функция правдопо-
добия? Найдите методом максимального правдоподобия оценку параметра $\theta$ равномерного распределения $U([\theta; \theta + 5])$.''',
                 r'''Пусть $X_1, ..., X_n$ - выборка объёма $n$ из некоторого распределения $\mathcal L_\theta(X)$ и пусть $f(x, \theta)$ - плотность распределения СВ $X$, а $x_1, ..., x_n$ - реализация случайной выборки.

Тогда функция максимального правдоподобия MLE имеет вид:

$\color{orange}{L(x, \theta) = f(x_1, \theta) \cdot\ ...\ \cdot f(x_n, \theta)}$

<br>

**Вероястностный смысл MLE**

Если для двух значений $\theta_1$ и $\theta_2$ параметра $\theta$ выполняется условие

$L(x, \theta_1) > L(x, \theta_2)$,

то говорят, что значение $\theta_1$ "более правдоподобно", чем $\theta_2$.

<br>

**Как использовать метод MLE**

Для нахождения оптимальной оценки максимального правдоподобия $\hat\theta_{MLE}$ необходимо выполнение неравенства:

$\color{orange}{L\left(x, \hat\theta_{MLE}(x)\right) \geq L(x, \theta)\ для\ \forall \theta \in \Theta}$

Иными словами, максимум функции правдоподобия достигается в точке, удовлетворяющей уравнению:

$\color{orange}{\frac{\partial L(x, \theta)}{\partial \theta} = 0}$ или $\color{orange}{\frac{\partial lnL(x, \theta)}{\partial \theta} = 0}$

<br>

**Пример**

Плотность равномерного закона $U([\theta; \theta+5])$:

$f(x, \theta) = \begin{cases}
\frac15,\ x\in[\theta; \theta+5];\\
0,\ otherwise\\
\end{cases}$

Составим функцию максимального правдоподобия:

$L(x, \theta) = f(x_1, \theta)\cdot\ ...\ \cdot f(x_n, \theta) = \begin{cases}
\left(\frac15\right)^n,\ x\in[\theta; \theta+5];\\
0,\ otherwise\\
\end{cases}$

Имеем вариационный ряд:

$\theta \leq X_{(1)} \leq ... \leq X_{(n)} \leq \theta + 5$

Тогда:

$\theta \leq X_{(1)}$

$\theta + 5 \geq X_{(n)}, \theta \geq X_{(n)} - 5$

Таким образом,

$\hat\theta_{MLE} \in [x_{(n)} - 5; x_{(1)}]$ - любая оценка из этого интервала является оптимальной.

<hr>'''),
            22:
                (r'''Как производится оценка параметров распределения методом моментов? Найдите методом мо-
ментов оценку параметра $\theta$ равномерного распределения $U([−\theta; \theta])$.''',
                 r'''**Суть метода моментов ММ**

Пусть $X_1, ..., X_n$ - выборка объёма $n$ из некоторого распределения $\mathcal L_\theta(X)$.

Положим, у наблюдаемой СВ $X$ существуют начальные моменты:

$\nu_k = E_\theta(X^k)$

Рассмотрим соответствующие эмпирические начальные моменты k-го порядка:

$\hat \nu_k = \overline{X^k}$

Составим систему уравнений относительно $\theta$:

$\nu_k(\theta) = \hat\theta_k,\ k=1,2,...$

Предположим, что система однозначно разрешима относительно $\theta$, тогда решение системы $\hat\theta_{ММ}$ будет называться оценкой параметра $\theta$, полученная методом моментов по k-ому порядку.

<br>

**Замечания**

- Метод моментов неприменим, когда теоретические моменты $\nu_k$ не существуют (например, для распределения Коши)

- Оценки ММ "мало эффективны"

- Оценка ММ обладает состоятельностью и асимптотической нормальностью

<br>

**Пример**

$\nu_1 = E(X) = \frac{a+b}{2} =\frac{-\theta + \theta}{2} = 0$
$Var(X) = \frac{(b-a)^2}{12} = \frac{(\theta + \theta)^2}{12}=\frac{\theta^2}{3}$

Составим систему уравнений:
$\begin{cases}
E(X) = \overline X,\\
Var(X) = \widehat{Var}(X).\\
\end{cases}$

Так как в E(X) отсутствует параметр , то выразим его из последнего уравнения:

$\frac{\theta^2}{3}=\hat \sigma^2$

$\hat \theta= \sqrt 3 \hat\sigma$

<hr>'''),
            23:
                (r'''Сформулируйте определение доверительной оценки параметра с коэффициентом доверия $\gamma$. Какой интервал называется асимптотически доверительным. Что такое точность доверительной оценки?''',
                 r'''Пусть $a \in (0;1)$ - некоторое число. Две статистики
<br>
$$\hat{\theta}_{1,n} = T_1(X_1, ..., X_n)$$
<br>
$$\hat{\theta}_{2,n} = T_2(X_1, ..., X_n)$$
<br>
определяют границы доверительного интервала $(\hat{\theta}_{1,n};(\hat{\theta}_{2,n})$ с коэффициентом доверия $\gamma = 1-a$, если при всех $\theta \in \Theta$ для выборки $X_1, ..., X_n \text{ из } \mathcal{L}_\theta(X)$ справедливо неравенство
<br>
$$P(\hat{\theta}_{1,n} < \theta < \hat{\theta}_{2,n}) \geq \underbrace{1-a}_\gamma$$
<br>
Коэффициент доверия $\gamma = 1-a$ иногда называют надежностью.
<br>
Доверительный интервал $(\hat{\theta}_{1,n};(\hat{\theta}_{2,n})$ называется точным, если для $\forall\theta \in \Theta$
<br>
$$P(\theta \in (\hat{\theta}_{1,n};\hat{\theta}_{2,n}) = \gamma$$
<br>
Доверительный интервал $(\hat{\theta}_{1,n};(\hat{\theta}_{2,n})$ называется асимптотическим , если:
<br>
$$P(\hat{\theta}_{1,n} < \theta < \hat{\theta}_{2,n}) \xrightarrow[n\to+\infty]{}\gamma$$
<br>
Для доверительного интервала $(\hat{\theta}_1;\hat{\theta}_2)$ его середину
<br>
$$\hat{\theta} = \frac{1}{2}(\hat{\theta}_1 + \hat{\theta}_2)$$
<br>
можно рассматривать как точечную оценку параметра $\theta$.
<br>
Величина $\varepsilon = \frac{1}{2}(\hat{\theta}_2 - \hat{\theta}_1)$ называется точностью доверительной оценки

<hr>'''),
            24:
                (r'''Приведите формулы (с выводом) доверительного точного интервала для параметра сдвига $\theta = \mu$ нормальной модели $N(\mu; \sigma^2)$, когда параметр масштаба $\sigma^2$ известен. Является ли такой интервал симметричным по вероятности? Ответ обосновать.''',
                 r'''Мы знаем, что
<br>
$ \frac{(\overline{X} - \theta)\sqrt{n}}{\sigma} \sim \mathcal{N}(0; 1)$
<br>
Учитывая это составим следующее вероятностное равенство, взяв доверительну вероятность, равную $1-\alpha$
<br>
$ P(|\frac{(\overline{X} - \theta)\sqrt{n}}{\sigma}|<u)=$
$ 1- P(|\frac{(\overline{X} - \theta)\sqrt{n}}{\sigma}|\geq u) = 1 - \alpha => P(|\frac{(\overline{X} - \theta)\sqrt{n}}{\sigma}|\geq u) = \alpha$
<br>
Откуда $u = z_{\frac{\alpha}{2}}$ из определения верхней процентной точки, учитывая, что z - симметрично
<br>
Рассмотрим это равенство, учитывая это:
$ P(\overline{X} - z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}<\mu<\overline{X} + z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}) = 1 - \alpha$
учитывая это, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = \overline{X} - z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}$
<br>
$
\hat{\theta}_{2, n} = \overline{X} + z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}$
<br>
Доказательство:
<br>
$ P(\hat{\theta}_{1, n} < \theta < \hat{\theta}_{2, n})
= P(\overline{X} - z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}<\mu<\overline{X} + z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}
= P(\mu - z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}}<\overline{X}<\mu + z_{\frac{\alpha}{2}} \cdot \frac{\sigma}{\sqrt{n}})
= P(-z_{\frac{\alpha}{2}} < \frac{(\overline{X} - \theta)\sqrt{n}}{\sigma} < z_{\frac{\alpha}{2}})
= F_Z(z_{\frac{\alpha}{2}}) - F_Z(-z_{\frac{\alpha}{2}}) = 
= F_Z(z_{\frac{\alpha}{2}}) - F_Z(z_{1 - \frac{\alpha}{2}})
= 1 - \frac{\alpha}{2} - \frac{\alpha}{2} = 1 - \alpha = \gamma
$
<br>
Чтобы проверить симметричность по вероятности, найду $P(\theta < \hat{\theta}_{2, n})$ и $P(\theta > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(\theta < \hat{\theta}_{2, n}) = P(\theta < \overline{X} + z_{\frac{\alpha}{2}}\cdot\frac{\sigma}{\sqrt{n}})
= P( \frac{(\overline{X} - \theta)\sqrt{n}}{\sigma} > -z_{\frac{\alpha}{2}}) = P(Z > -z_{\frac{\alpha}{2}}) = 1 - P(Z \leq -z_{\frac{\alpha}{2}}) = 1 - Z(-z_{\frac{\alpha}{2}}) = 1 - \frac{\alpha}{2}$
<br>
$P(\theta > \hat{\theta}_{1, n}) = P(\theta > \overline{X} - z_{\frac{\alpha}{2}}\cdot\frac{\sigma}{\sqrt{n}})
= P( \frac{(\overline{X} - \theta)\sqrt{n}}{\sigma} < z_{\frac{\alpha}{2}}) = P(Z < z_{\frac{\alpha}{2}}) = 1 - P(Z \geq z_{\frac{\alpha}{2}}) = 1 - \frac{\alpha}{2}$
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            25:
                (r'''Приведите формулы (с выводом) доверительного точного интервала для параметра масштаба $\theta = \sigma^2$ нормальной модели $N(\mu; \sigma^2)$, когда значение параметра сдвига $\mu$ известно. Является ли такой
интервал симметричным по вероятности? Ответ обосновать.''',
                 r'''Так как нам неизвестна дисперсия, вместо неё будем использовать следующую оценку:
<br>
$ s_0^2 = \frac{1}{n}\sum\limits_{k=1}^n(X_k-\mu)^2$, где $\mu$ - известно
<br>
Если $H_0$ верна, то T статистика = $\frac{ns_0^2}{\theta} = \sum\limits_{k=1}^nZ_k^2$ $\sim \chi^2(n) $
<br>
Учитывая это составим следующее вероятностное равенство, взяв уровень значимости, равный $\alpha$
<br>
$ P(|\frac{ns_0^2}{\theta}|<u)=$
$ 1- P(|\frac{ns_0^2}{\theta}|\geq u) = 1 - \alpha$
<br>
Откуда $P(|\frac{ns_0^2}{\theta}|\geq u) = \alpha$,тогда, по определению верхней процентной точки и учитывая, что $\chi^2$ - несимметричное, получим:
$P(\frac{ns_0^2}{\theta}\geq u) = {\frac{\alpha}{2}} => u = \chi^2_{\frac{\alpha}{2}}(n)$
<br>
$P(\frac{ns_0^2}{\theta}\leq -u) = 1 - P(\frac{ns_0^2}{\theta}\geq u) = 1 - \frac{\alpha}{2}=> u = \chi^2_{1 - \frac{\alpha}{2}}(n)$
<br>
Рассмотрим это равенство, учитывая это. (при переносе из знаменателя оцениваемого параметра, $\chi$ с $1 - \frac{\alpha}{2}$ и $\frac{\alpha}{2}$ поменяются местами!)
<br>
Получим:
$ P(\frac{ns^2_0}{\chi^2_{\frac{\alpha}{2}}(n)}<\sigma^2<\frac{ns^2_0}{\chi^2_{1 - \frac{\alpha}{2}}(n)}) = 1 - \alpha$
<br>
Тогда, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = \frac{ns^2_0}{\chi^2_{\frac{\alpha}{2}}(n)}$
<br>
$
\hat{\theta}_{2, n} = \frac{ns^2_0}{\chi^2_{1-\frac{\alpha}{2}}(n)}$
<br>
Доказательство:
<br>
$ P(\hat{\theta}_{1, n} < \theta < \hat{\theta}_{2, n})
= P(\frac{ns^2_0}{\chi^2_{\frac{\alpha}{2}}(n)}<\sigma^2<\frac{ns^2_0}{\chi^2_{1-\frac{\alpha}{2}}(n)})
= P(\chi^2_{1-\frac{\alpha}{2}}(n) < \frac{ns^2_0}{\sigma^2} < \chi^2_{\frac{\alpha}{2}}(n))
= F_{T_0}(\chi^2_{\frac{\alpha}{2}}(n)) - F_{T_0}(\chi^2_{1-\frac{\alpha}{2}}(n)) = 1 - \frac{\alpha}{2}
- (1 - (1 - \frac{\alpha}{2})) = 1 - \alpha = \gamma
$
<br>
Чтобы проверить симметричность по вероятности, найду $P(\sigma^2 < \hat{\theta}_{2, n})$ и $P(\sigma^2 > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(\sigma^2 < \hat{\theta}_{2, n}) = P(\theta < \frac{ns^2_0}{\chi^2_{1-\frac{\alpha}{2}}(n)})
= P(\chi^2_{1-\frac{\alpha}{2}}(n) < \frac{ns^2_0}{\theta})
 = P(\chi^2_{1-\frac{\alpha}{2}}(n) < \chi^2(n))
 = 1 - \frac{\alpha}{2}$
<br>
$P(\sigma^2 > \hat{\theta}_{2, n}) = P(\theta > \frac{ns^2_0}{\chi^2_{\frac{\alpha}{2}}(n)})
= 1 - P(\chi^2_{\frac{\alpha}{2}}(n) \leq \frac{ns^2_0}{\theta})
= 1 - P(\chi^2_{\frac{\alpha}{2}}(n) \leq \chi^2(n))
= 1 - \frac{\alpha}{2}$
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            26:
                (r'''Приведите формулы (с выводом) доверительного точного интервала для параметра сдвига $\theta = \mu$
нормальной модели $N(\mu; \sigma^2)$, когда параметр масштаба $\sigma^2$– неизвестен. Является ли такой интер-
вал симметричным по вероятности? Ответ обосновать.''',
                 r'''Так как нам неизвестна дисперсия, вместо неё будем использовать следующую оценки:
<br>
$\overline{X} = \frac{1}{n}\sum\limits_{k=1}^nX_k$
<br>
$ s_0^2 = \frac{1}{n-1}\sum\limits_{k=1}^n(X_k-\overline{X})^2$
<br>
Если $H_0$ верна, то $T \sim \mathcal{t}(n - 1) $
<br>
Учитывая это составим следующее вероятностное равенство, взяв доверительну вероятность, равную $1-\alpha$
<br>
$ P(|\frac{(\overline{X} - \theta)\sqrt{n}}{s}|<u)=$
$ 1- P(|\frac{(\overline{X} - \theta)\sqrt{n}}{s}|\geq u) = 1 - \alpha => P(|\frac{(\overline{X} - \theta)\sqrt{n}}{s}|\geq u) = \alpha$
<br>
Откуда $u = t(n-1)_{\frac{\alpha}{2}}$ из определения верхней процентной точки, учитывая, что t - симметрично
<br>
Рассмотрим это равенство, учитывая это:
$ P(\overline{X} - t(n-1)_{\frac{\alpha}{2}} \cdot \frac{s}{\sqrt{n}}<\mu<\overline{X} + t(n-1)_{\frac{\alpha}{2}} \cdot \frac{s}{\sqrt{n}}) = 1 - \alpha$
учитывая это, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = \overline{X} - t(n-1)_{\frac{\alpha}{2}} \cdot \frac{s}{sqrt{n}}$
<br>
$
\hat{\theta}_{2, n} = \overline{X} + t(n-1)_{\frac{\alpha}{2}} \cdot \frac{s}{\sqrt{n}}$
<br>
Доказательство:
<br>
$ P(\hat{\theta}_{1, n} < \theta < \hat{\theta}_{2, n})
= P(\overline{X} - t(n-1)_{\frac{\alpha}{2}} \cdot \frac{s}{\sqrt{n}}<\mu<\overline{X} + t_{\frac{\alpha}{2}} \cdot \frac{s}{\sqrt{n}})
= P(-t(n-1)_{\frac{\alpha}{2}} < \frac{(\overline{X} - \theta)\sqrt{n}}{s} < t(n-1)_{\frac{\alpha}{2}})
= F_T(t_{\frac{\alpha}{2}}) - F_T(-t_{\frac{\alpha}{2}}) = 1 - \frac{\alpha}{2}
 - (1 - (1 - \frac{\alpha}{2})) = 1 - \alpha = \gamma
$
<br>
Чтобы проверить симметричность по вероятности, найду $P(\theta < \hat{\theta}_{2, n})$ и $P(\theta > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(\theta < \hat{\theta}_{2, n}) = P(\theta < \overline{X} + t(n-1)_{\frac{\alpha}{2}}\cdot\frac{s}{\sqrt{n}})
= P( \frac{(\overline{X} - \theta)\sqrt{n}}{s} > -t(n-1)_{\frac{\alpha}{2}}) = P(T > -t(n-1)_{\frac{\alpha}{2}}) = 1 - P(T \leq -t(n-1)_{\frac{\alpha}{2}}) = 1 - T(-t(n-1)_{\frac{\alpha}{2}}) = 1 - \frac{\alpha}{2}$
<br>
$P(\theta > \hat{\theta}_{1, n}) = P(\theta > \overline{X} - t(n-1)_{\frac{\alpha}{2}}\cdot\frac{s}{\sqrt{n}})
= P( \frac{(\overline{X} - \theta)\sqrt{n}}{s} < t(n-1)_{\frac{\alpha}{2}}) = P(T < t(n-1)_{\frac{\alpha}{2}}) = 1 - P(T \geq t(n-1)_{\frac{\alpha}{2}}) = 1 - \frac{\alpha}{2}$
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            27:
                (r'''Приведите формулы (с выводом) доверительного точного интервала для параметра масштаба $\theta = \sigma^2$ нормальной модели $N(\mu; \sigma^2)$, когда параметр сдвига $\mu$ – неизвестен. Является ли такой интервал
симметричным по вероятности? Ответ обосновать.''',
                 r'''Так как нам неизвестна дисперсия и также неизвестно математическое ожидание, будем использовать следующую случайную величину:
<br>
$ \hat{\theta_n} = \frac{(n-1)s^2}{\sigma^2} = \frac{(X_1 - \overline{X})^2+ ... + (X_n - \overline{X})^2}{\sigma^2}$
<br>
по теореме Фишера $\hat{\theta_n} \sim \chi^2(n-1) $
<br>
Учитывая это составим следующее вероятностное равенство, взяв уровень значимости, равный $\alpha$
<br>
$ P(|\frac{(n-1)s_0^2}{\theta}|<u)=$
$ 1- P(|\frac{(n-1)s_0^2}{\theta}|\geq u) = 1 - \alpha => P(|\frac{(n-1)s_0^2}{\theta}|\geq u) = \alpha$
<br>
Откуда:
<br>
$P(\frac{ns_0^2}{\theta}\geq u) = {\frac{\alpha}{2}} => u = \chi^2_{\frac{\alpha}{2}}(n)$
<br>
$P(\frac{ns_0^2}{\theta}\leq -u) = 1 - P(\frac{ns_0^2}{\theta}\geq u) = 1 - \frac{\alpha}{2}=> u = \chi^2_{1 - \frac{\alpha}{2}}(n)$
<br>
Рассмотрим это равенство, учитывая это. (при переносе из знаменателя оцениваемого параметра, $\chi$ с $1 - \frac{\alpha}{2}$ и $\frac{\alpha}{2}$ поменяются местами!)
<br>
$P(\frac{(n-1)s_0^2}{\theta}\geq -u) = 1 - P(\frac{(n-1)s_0^2}{\theta}\geq u) =1 - (1 - {\frac{\alpha}{2}}) => u = \chi^2_{\frac{\alpha}{2}}(n-1)$
<br>
Рассмотрим это равенство, учитывая это. Получим:
$ P(\frac{(n-1)s^2_0}{\chi^2_{\frac{\alpha}{2}}(n-1)}<\sigma^2<\frac{(n-1)s^2_0}{\chi^2_{1 - \frac{\alpha}{2}}(n-1)}) = 1 - \alpha$
<br>
Тогда, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = \frac{(n-1)s^2_0}{\chi^2_{\frac{\alpha}{2}}(n-1)}$
<br>
$
\hat{\theta}_{2, n} = \frac{(n-1)s^2_0}{\chi^2_{1-\frac{\alpha}{2}}(n-1)}$
<br>
Доказательство:
<br>
$ P(\hat{\theta}_{1, n} < \theta < \hat{\theta}_{2, n})
= P(\frac{(n-1)s^2_0}{\chi^2_{\frac{\alpha}{2}}(n-1)}<\sigma^2<\frac{(n-1)s^2_0}{\chi^2_{1-\frac{\alpha}{2}}(n-1)})
= P(\chi^2_{1-\frac{\alpha}{2}}(n-1) < \frac{(n-1)s^2_0}{\sigma^2} < \chi^2_{\frac{\alpha}{2}}(n-1))
= F_{\hat{\theta}_n}(\chi^2_{\frac{\alpha}{2}}(n-1)) - F_{\hat{\theta}_n}(\chi^2_{1-\frac{\alpha}{2}}(n-1)) = 1 - \frac{\alpha}{2}
- (1 - (1 - \frac{\alpha}{2})) = 1 - \alpha = \gamma
$
<br>
Чтобы проверить симметричность по вероятности, найду $P(\sigma^2 < \hat{\theta}_{2, n})$ и $P(\sigma^2 > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(\sigma^2 < \hat{\theta}_{2, n}) = P(\theta < \frac{ns^2_0}{\chi^2_{1-\frac{\alpha}{2}}(n)})
= P(\chi^2_{1-\frac{\alpha}{2}}(n-1) < \frac{(n-1)s^2_0}{\theta})
 = P(\chi^2_{1-\frac{\alpha}{2}}(n-1) < \chi^2(n-1))
 = 1 - \frac{\alpha}{2}$
<br>
$P(\sigma^2 > \hat{\theta}_{1, n}) = P(\theta > \frac{(n-1)s^2_0}{\chi^2_{\frac{\alpha}{2}}(n-1)})
= 1 - P(\chi^2_{\frac{\alpha}{2}}(n-1) \leq \frac{(n-1)s^2_0}{\theta})
= 1 - P(\chi^2_{\frac{\alpha}{2}}(n-1) \leq \chi^2(n-1))
= 1 - \frac{\alpha}{2}$
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            28:
                (r'''Сформулируйте теорему Фишера. Пусть $X_1,X_2, . . . X_n$ – выборка объема n из $N(\mu; \sigma^2)$. Найдите а) Cov($X_i - \overline X; \overline X); б) Cov(X_i- \overline X; X_j - \overline X), i \neq j.$''',
                 r'''Теорема Роналда Фишера
<br>
1) Статистики $\overline{X}$ и $s^2$ - независимы
<br>
2) $\overline{X} \sim \mathcal{N}(\mu; \frac{\sigma^2}{n})$
<br>
3) $ \frac{(n-1)s^2}{\sigma^2} \sim \chi(n-1)$

<br>

Свойство ковариации:

$Cov(a + b; c) = Cov(a; c) + Cov(b; c)$

Если $a$ и $b$ независимы, то $Cov(a; b) = 0$

<br>

a) $ Cov(X_i - \overline{X}, \overline{X}) = Cov(X_i, \overline{X}) - Cov(\overline{X}, \overline{X})
= Cov(X_i, \frac{1}{n} \sum\limits_{j=1}^nX_j) - Var(\overline{X}) =
\frac{1}{n} \sum\limits_{i=1}^nCov(X_i, X_j) - \frac{\sigma^2}{n}
= \frac{1}{n} Cov(X_i, X_i) - \frac{\sigma^2}{n} =
\frac{\sigma^2}{n} - \frac{\sigma^2}{n} = 0$,
что совпадает с 1 пунктом из теоремы Фишера.

<br>

б) Используя результаты пункта а):

$ Cov(X_i - \overline{X}, X_j - \overline{X})
= Cov(X_i, X_j) - Cov(X_i, \overline{X}) - Cov(X_j, \overline{X}) + Cov(\overline{X}, \overline{X})
$<br>$
= 0 - \frac{\sigma^2}{n} - \frac{\sigma^2}{n}  + Var(\overline{X})$
$=  - \frac{2 \sigma^2}{n} + \frac{\sigma^2}{n}
= - \frac{\sigma^2}{n}$

<hr>'''),
            29:
                (r'''Приведите формулы (с выводом) доверительного точного интервала предсказания для $X_{n+1}$ по выборке $X_1, X_2, . . . , X_n$ из нормальной модели $N(\mu; \sigma^2)$, когда оба параметр $\mu$ и $\sigma^2$– неизвестны. Является ли такой интервал симметричным по вероятности? Ответ обосновать.''',
                 r'''Введём следующую случайную величину:
$ T = \frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}}$, где $\overline{X} = \frac{1}{n} \sum\limits_{k=1}^n X_k$ - выборочное среднее, $s^2 = \frac{1}{n-1} \sum\limits_{k=1}^n (X_k - \overline{X})^2$ - исправленная выборочная дисперсия

$T = \frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}} =
\frac{\frac{X_{n+1}-\overline{X}}{\sigma\sqrt{1 + \frac{1}{n}}}}{\sqrt{\frac{(n-1)s^2}{\sigma^2} \cdot \frac{1}{n-1}}}
$(под корнем в знаменателе теорема Фишера)$
=\frac{Z_0}{\sqrt{\frac{\chi_{n-1}^2}{n-1}}} = \frac{Z_0\sqrt{n-1}}{\sqrt{\chi_{n-1}^2}} \sim t(n-1)$
<br>
Учитывая это составим следующее вероятностное равенство, взяв уровень значимости, равный $\alpha$
<br>
$ P(|\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}}|<u)=$
$ 1- P(|\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}}|\geq u) = 1 - \alpha$
<br>
Откуда $P(|\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}}|\geq u) = \alpha$,тогда, по определению верхней процентной точки и учитывая, что t - симметричное, получим:
u = $t_{\frac{\alpha}{2}}$
<br>
Рассмотрим это равенство, учитывая это. Выразим $X_{n+1}$ и получим:
$ P(\overline{X} - t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}}<X_{n+1}<\overline{X} + t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}}) = 1 - \alpha$
<br>
Тогда, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = \overline{X} - t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}}$
<br>
$
\hat{\theta}_{2, n} = \overline{X} + t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}}$
<br>
Доказательство:
<br>
$ P(\hat{\theta}_{1, n} < X_{n+1} < \hat{\theta}_{2, n})
= P(\overline{X} - t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}}<X_{n+1}<\overline{X} + t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}})
= P(-t_{\frac{\alpha}{2}}(n-1) < \frac{X_{n+1} - \overline{X}}{s\sqrt{1 + \frac{1}{n}}} < t_{\frac{\alpha}{2}}(n-1))
= F_T(t_{\frac{\alpha}{2}}(n-1)) - F_T(-t_{\frac{\alpha}{2}}(n-1))
= F_T(t_{\frac{\alpha}{2}}(n-1)) - F_T(1-t_{\frac{\alpha}{2}}(n-1))
= 1 - \frac{\alpha}{2}
- (1 - (1 - \frac{\alpha}{2})) = 1 - \alpha = \gamma
$
<br>
Чтобы проверить симметричность по вероятности, найду $P(\sigma^2 < \hat{\theta}_{2, n})$ и $P(\sigma^2 > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(X_{n+1} < \hat{\theta}_{2, n}) = P(X_{n+1} < \overline{X} + t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}})
= P(\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}} < t_{\frac{\alpha}{2}}(n-1))
 = 1 - P(\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}} \geq t_{\frac{\alpha}{2}}(n-1))
 = 1 - \frac{\alpha}{2}$
<br>
$P(X_{n+1} > \hat{\theta}_{1, n}) = P(X_{n+1} > \overline{X} - t_{\frac{\alpha}{2}}(n-1)s\sqrt{1+\frac{1}{n}})
= P(\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}} > -t_{\frac{\alpha}{2}}(n-1))
= P(\frac{X_{n+1}-\overline{X}}{s\sqrt{1 + \frac{1}{n}}} > t_{1 - \frac{\alpha}{2}}(n-1))
 = 1 - \frac{\alpha}{2}$
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            30:
                (r'''Дайте определение асимптотического доверительного интервала и приведите формулы (с выводом) асимптотического доверительного интервала для коэффициента корреляции ρ по выборке $(X_1; Y_1),(X_2; Y_2), . . .(X_n; Y_n)$ объема n из двумерной нормальной модели $N(\mu_1; \mu_2; \sigma^2_1;\sigma^2_2; \rho)$. Является ли такой интервал симметричным по вероятности? Ответ обосновать.''',
                 r'''Асимптотический доверительный интервал это такой интервал $(\hat{\theta}_{1, n}, \hat{\theta}_{2, n})$, что $P(\hat{\theta}_{1, n} < \theta < \hat{\theta}_{2, n}) \xrightarrow[n\to\infty] {} \gamma = 1 - \alpha$
<br>
Для оценки неизвестного параметра используем выборочный коэффициент корреляции :
$ \hat{\rho_n} = \frac{\hat{Cov}(X, Y)}{\sqrt{\sigma^2_X} \cdot \sqrt{\sigma^2_Y}}$

Следующая оценка с $\sigma^2(\rho) = \frac{(1-\rho^2)^2}{n}$ будет асимптотически нормальна:
$ \frac{\sqrt{n}(\hat{\rho} - \rho)}{\sigma^2_{\rho}}
= \frac{n(\hat{\rho} - \rho)}{1 - \rho^2}
\xrightarrow[n\to\infty] d \sim \mathcal{N}(0; 1) $, но при близких к 0 и 1 значения сильно отличается от нормального распределения, из-за чего Фишер предложил следующее Z-преобразование:

$\hat{Z}_n = arth(\hat{\rho}_n) = \frac12 \ln \frac{1 + \hat{\rho}}{1 - \hat{\rho}}$, откуда $ \sqrt{n-3}(\hat{Z}_n - arth(\rho)) \xrightarrow[n\to\infty] d \sim \mathcal{N}(0; 1)$
<br>
Учитывая это составим следующее вероятностное равенство, взяв доверительную вероятность, равную 1 - $\alpha$
<br>
$ P(|\sqrt{n-3}(\hat{Z}_n - arth(\rho)) |<u)=$
$ 1- P(|\sqrt{n-3}(\hat{Z}_n - arth(\rho)) |\geq u) = 1 - \alpha$
<br>
Откуда $P(|\sqrt{n-3}(\hat{Z}_n - arth(\rho))|\geq u) = \alpha$,тогда, по определению верхней процентной точки и учитывая, что нормальное распределение симметричное, получим:
u = $z_{\frac{\alpha}{2}}$
<br>
Рассмотрим исходное вероятностное равенство, учитывая это и выразим $\rho$:
<br>
$ \sqrt{n-3}(\hat{Z}_n - arth(\rho)) < z_{\frac{\alpha}{2}}$
<br>
$ (\hat{Z}_n - arth(\rho)) < \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}}$
<br>
$ arth(\rho) \geq -\frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}} + \hat{Z}_n$
<br>
$ \rho \geq th(\hat{Z}_n - \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})$
<br>
и
<br>
$ \sqrt{n-3}(\hat{Z}_n - arth(\rho)) > -z_{\frac{\alpha}{2}}$
<br>
$ (\hat{Z}_n - arth(\rho)) > -\frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}}$
<br>
$ arth(\rho) \leq \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}} + \hat{Z}_n$
<br>
$ \rho \leq th(\hat{Z}_n + \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}} + )$
<br>
Тогда, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = th(\hat{Z}_n - \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})
= th(arth(\hat{\rho}_n) - \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})$
<br>
$
\hat{\theta}_{2, n} = th(\hat{Z}_n + \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})
= th(arth(\hat{\rho}_n) + \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})$

<br>

Чтобы проверить симметричность по вероятности, найду $P(\sigma^2 < \hat{\theta}_{2, n})$ и $P(\sigma^2 > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(\theta < \hat{\theta}_{2, n}) = P(\rho < th(arth(\hat{\rho}_n) + \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}}))
= P(arth(\rho) < arth(\hat{\rho}_n) + \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})
= P(- \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}} < arth(\hat{\rho}_n) - arth(\rho))
= P(- z_{\frac{\alpha}{2}} < \sqrt{n-3} \cdot (arth(\hat{\rho}_n) - arth(\rho)))
= P(- z_{\frac{\alpha}{2}} < Z)
= P(z_{1 - \frac{\alpha}{2}} < Z) = 1 - \frac{\alpha}{2}$
<br>
$P(\theta > \hat{\theta}_{1, n}) = P(\rho > th(arth(\hat{\rho}_n) - \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}}))
= P(arth(\rho) > arth(\hat{\rho}_n) - \frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}})
= P(\frac{1}{\sqrt{n-3}}z_{\frac{\alpha}{2}} > arth(\hat{\rho}_n) - arth(\rho))
= P(z_{\frac{\alpha}{2}} > \sqrt{n-3} \cdot (arth(\hat{\rho}_n) - arth(\rho)))
= P(z_{\frac{\alpha}{2}} > Z)
= 1 - P(z_{\frac{\alpha}{2}} < Z)
= 1 - \frac{\alpha}{2}$
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            31:
                (r'''Дайте определение асимптотического доверительного интервала и приведите формулы (с выводом) асимптотического доверительного интервала для парамера вероятности $\theta$ = p. Выведите уравнение доверительного эллипса.''',
                 r'''Асимптотический доверительный интервал это такой интервал $(\hat{\theta}_{1, n}, \hat{\theta}_{2, n})$, что $P(\hat{\theta}_{1, n} < \theta < \hat{\theta}_{2, n}) \xrightarrow[n\to\infty] {} \gamma = 1 - \alpha$
<br>
Зададим доверительную вероятеость $\gamma = 1 - \alpha$ и попытаемся найти такое $\varepsilon$, чтобы $P(|\hat{p} - p|<\varepsilon) \xrightarrow[n\to\infty] {} \gamma = 1 - \alpha$ или же при достаточно больших n $P(|\hat{p} - p|<\varepsilon) \approx \gamma = 1 - \alpha$
<br>
$P(|\hat{p} - p|<\varepsilon)
= P(p-\varepsilon<\hat{p}<p+\varepsilon)
\approx |\hat{p} \approx \mathcal{N}(p; \frac{p(1-p)}{n})|
\approx \Phi_0(\frac{p + \varepsilon - p}{\sqrt{\frac{p(1-p)}{n}}}) - \Phi_0(\frac{p + \varepsilon - p}{\sqrt{\frac{p(1-p)}{n}}})
=2\Phi_0(\frac{\varepsilon}{\sqrt{\frac{p(1-p)}{n}}})$,
где $\Phi_0$ - функция Лапласа
<br>
$2\Phi_0(\frac{\varepsilon}{\sqrt{\frac{p(1-p)}{n}}}) \approx
\gamma = 1 - \alpha => \Phi_0(\frac{\varepsilon}{\sqrt{\frac{p(1-p)}{n}}}) \approx \frac{\gamma}{2}$, решением этого уравнения является $z_{\frac{\alpha}{2}}
=\Phi^{-1}_0(\frac{\gamma}{2}) => z_{\frac{\alpha}{2}} = \frac{\varepsilon}{\sqrt{\frac{p(1-p)}{n}}}$
<br>
$\varepsilon = z_{\frac{\alpha}{2}} \cdot \sqrt{\frac{p(1-p)}{n}}$, подставляя в исходно заданную вероятность получим:
$P(|\hat{p} - p|<\varepsilon) = P(|\hat{p} - p|<z_{\frac{\alpha}{2}} \cdot \sqrt{\frac{p(1-p)}{n}})$, что равносильно следующему неравенству:
<br>
$(\hat{p} - p)^2 < \frac{z_{\frac{\alpha}{2}}}{n}p(1-p)$
<br>
Рассматривая плоскость Oxy, где $x = \hat{p}, y = p$ получим геометрическое место точек, удовлетворяющее следующему неравенству:
<br>
$(x - y)^2 < \frac{z_{\frac{\alpha}{2}}}{n}y(1-y)$
<br>
Это ГМТ называется доверительным эллипсом.
<br>
Вернёся к неравенству $(\hat{p} - p)^2 < \frac{z_{\frac{\alpha}{2}}}{n}p(1-p)$ и перепишем его относительно p:
$(1 + \frac{z_{\frac{\alpha}{2}}}{n}) \cdot p^2 - (2\hat{p}+\frac{z_{\frac{\alpha}{2}}}{n}) \cdot p + \hat{p}^2 < 0$
<br>
Решив это неравенство получим следующие доверительные интервалы:
<br>
```
n, p, p_h, z = sp.symbols('n, p, \hat{p}, z_{a/2}')

sp.solve((1 + z/n)*p**2 - (2*p_h + z/n) * p + p_h**2, p)[0]

sp.solve((1 + z/n)*p**2 - (2*p_h + z/n) * p + p_h**2, p)[1]
```
<br>
$\hat{\theta}_{1, n} =
\frac{\hat{p} + \frac{z_{\frac{\alpha}{2}}}{n}
- z_{\frac{\alpha}{2}} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z_{\frac{\alpha}{2}}}{4n^2}}}
{1 + \frac{z_{\frac{\alpha}{2}}}{n}}$
<br>
$\hat{\theta}_{2, n} =
\frac{\hat{p} + \frac{z_{\frac{\alpha}{2}}}{n}
+ z_{\frac{\alpha}{2}} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z_{\frac{\alpha}{2}}}{4n^2}}}
{1 + \frac{z_{\frac{\alpha}{2}}}{n}}$
<br>
При n>>100 используют приближённый доверительный интервал
<br>
$\hat{\theta}_{1, n} \approx
\hat{p} - z_{\frac{\alpha}{2}} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$
<br>
$\hat{\theta}_{1, n} \approx
\hat{p} + z_{\frac{\alpha}{2}} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$
<br>
Тогда $(\hat{\theta}_{1, n}, \hat{\theta}_{2, n})$ является асимптотическим доверительным интервалом для парамера вероятности $\theta$ = p

<hr>
<hr>'''),
            32:
                (r'''Пусть $X_j = (X_{1j} , X_{2j} , . . . , X_{n_jj} )$ – выборка объема $n_j$ из $N(\mu; \sigma^2)$, где j = 1, . . . , k. Приведите формулы (с выводом) доверительного интервала для параметра $\mu_j$ , используя в качестве несмещенной оценки параметра $\sigma^2$ остаточную дисперсию $\frac {1}{n-k}\sum_{j=1}^{k}\sum_{i=1}^{k}{(X_{ij}- \overline X_j)^2}$. Является ли такой интервал симметричным по вероятности? Ответ обосновать.''',
                 r'''Будем использвать следующую статистику для нахождения доверительных интервалов в <b>каждой</b> группе:
$ T_j = \frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}
= \frac{\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sigma}}
{\sqrt{\frac{(n-k)MSE}{\sigma^2} \cdot \frac{1}{n - k}}}
=\frac{Z_0}{\sqrt{\frac{\chi^2(n-k)}{n-k}}} \sim t(n-k)$
<br>
Учитывая это составим следующее вероятностное равенство, взяв доверительную вероятность, равную 1 - $\alpha$
<br>
$ P(|\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}|<u)=$
$ 1- P(|\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}|\geq u) = 1 - \alpha$
<br>
Откуда $P(|\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}|\geq u) = \alpha$,тогда, по определению верхней процентной точки и учитывая, что нормальное распределение симметричное, получим:
u = $t(n-k)_{\frac{\alpha}{2}}$
<br>
Рассмотрим исходное вероятностное равенство, учитывая это и выразим $\mu$:
<br>
$ \frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}} < t_{\frac{\alpha}{2}}$
<br>
$ (\overline{X_j} - \mu_j) < t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}}$
<br>
$ \mu_j \geq \overline{X_j} - t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}}$
<br>
и
<br>
$ \frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}} > -t_{\frac{\alpha}{2}}$
<br>
$ (\overline{X_j} - \mu_j) > -t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}}$
<br>
$ \mu_j \leq \overline{X_j} + t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}}$
<br>
Тогда, формулы для доверительного интервала:
<br>
$
\hat{\theta}_{1, n} = \overline{X_j} - t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}}$
<br>
$
\hat{\theta}_{2, n} = \overline{X_j} + t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}}$

<br>

Чтобы проверить симметричность по вероятности, найду $P(\mu < \hat{\theta}_{2, n})$ и $P(\mu > \hat{\theta}_{1, n})$, для симметричности необходимо их равенство
$P(\mu < \overline{X_j} + t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}})
= P(\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}  < t_{\frac{\alpha}{2}})
= 1 - P(\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}  \geq t_{\frac{\alpha}{2}})
= 1 - P(t(n-k) \geq t_{\frac{\alpha}{2}})
= 1 - \frac{\alpha}{2}$ из определения верхней процентной точки
<br>
$P(\mu > \overline{X_j} - t_{\frac{\alpha}{2}} \sqrt{\frac{MSE}{n_j}})
= P(\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}  > -t_{\frac{\alpha}{2}})
= P(\frac{\sqrt{n_j}(\overline{X_j} - \mu_j)}{\sqrt{MSE}}  > t_{1 - \frac{\alpha}{2}})
= 1 - P(t(n-k) > t_{1 - \frac{\alpha}{2}})
= 1 - \frac{\alpha}{2}$ из определения верхней процентной точки
<br>
$P(\theta < \hat{\theta}_{2, n}) = P(\theta > \hat{\theta}_{1, n})$, а следовательно данный доверительный интервал является симметричным по вероятности

<hr>'''),
            33:
                (r'''Пусть $X_j = (X_{1j} , X_{2j} , . . . , X_{n_jj} )$ – выборка объема $n_j$ из $N(\mu; \sigma^2)$, где j = 1, . . . , k. Приведите формулы (с выводом и необходимыми пояснениями в обозначениях) дисперсионного тождества.''',
                 r'''Формулы:
<br>
1. SSTOT = SSTR + SSE
<br>
2. $\hat{\sigma}^2 = \delta^2 + \overline{\sigma^2}$

$SSTOT$ - полная сумма квадратов отклонений
<br>
$SSTR$ - межгрупповая сумма квадратов
<br>
$SSE$ - внутригрупповая сумма квадратов
<br>
$\hat{\sigma}^2$ - выборочная дисперсия в <b>объединённой</b>
<br>
$\delta^2$ - межгрупповая дисперсия
<br>
$\overline{\sigma^2}$ - средняя групповая дисперсия

<br>

$SSTOT \stackrel{\color{lightgreen}{опр.}}{=} \sum\limits_{j=1}^k \sum\limits_{i=1}^{n_j}(X_{ij} - \overline{X})^2
=\sum\limits_{j=1}^k \sum\limits_{i=1}^{n_j} \left[(\overline{X_j} - \overline{X}) + (X_{ij} - \overline{X_j})\right]^2
= \sum\limits_{j=1}^k \sum\limits_{i=1}^{n_j} (\overline{X_j} - \overline{X})^2
+ \sum\limits_{j=1}^k \sum\limits_{i=1}^{n_j} (X_{ij} - \overline{X_j})^2
+ 2 \cdot \sum\limits_{j=1}^k \sum\limits_{i=1}^{n_j} (\overline{X_j} - \overline{X}) \cdot (X_{ij} - \overline{X_j})
= \sum\limits_{j=1}^k n_j \cdot (\overline{X_j} - \overline{X})^2
+ \stackrel{\color{lightgreen}{опр.}}{SSE}
+ 2 \cdot \sum\limits_{j=1}^k (\overline{X_j} - \overline{X}) \sum\limits_{i=1}^{n_j} (X_{ij} - \overline{X_j})
= \stackrel{\color{lightgreen}{опр.}}{SSTR} + SSE
+ 2 \cdot \sum\limits_{j=1}^k (\overline{X_j} - \overline{X}) ((\sum\limits_{i=1}^{n_j} X_{ij}) - n_j \cdot \overline{X_j})
= SSTR + SSE + 2 \cdot \sum\limits_{j=1}^k (\overline{X_j} - \overline{X}) (n_j \cdot \overline{X_j} - n_j \cdot \overline{X_j})
= SSTR + SSE + 0 = SSTR + SSE$

<br>

$SSTOT = n \cdot \hat{\sigma}^2$
<br>
$SSTR = n \cdot \delta^2$
<br>
$SSE = n \cdot \overline{\sigma^2}$

Разделив $SSTOT = SSTR + SSE$ на $n$ получим диспресионное тождество:
<br>
$\hat{\sigma}^2 = \delta^2 + \overline{\sigma^2}$

<hr>'''),
            34:
                (r'''Пусть $X_j = (X_{1j} , X_{2j} , . . . , X_{n_jj} )$ – выборка объема $n_j$ из $N(\mu; \sigma^2)$, где j = 1, . . . , k.
Дайте определениефакторной дисперсии. Приведите формулу (с выводом и необходимыми пояснениями в обозначениях) математического ожидания факторной дисперсии.''',
                 r'''Статистика ${MSTR} = \frac{SSTR}{k-1} = \frac{n\delta^2}{k-1} = \frac{1}{k-1} \sum\limits_{j=1}^k(\overline{X}_{j} - \overline{X})^2 \cdot n_j$, где $\delta^2$ - межгрупповая дисперсия, k - количество групп, $n_j$ - количество элементов в j-ой группе. Факторная дисперсия это несмещённая межгруповая сумма квадратов, то есть её вывод - удаление смещения из межгрупповой суммы квадратов путём добавления коэффициента $\frac{1}{k-1}$.

Для дальнейшего докажем один факт:
$\sum_{i=1}^{n}{(X_i - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X + \overline X - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X)^2} + 2\sum_{i=1}^{n}{(\overline X - \mu)(X_i - \overline X)} + \sum_{i=1}^{n}{(\overline X - \mu)^2} \stackrel{\color{lightgreen}{\sum (\overline X - \mu) = 0}}{=} \sum_{i=1}^{n}{(X_i - \overline X)^2} + n(\overline X - \mu)^2$

Рассмотрим математическое ожидание этой величины:
$ E(MSTR) = E\left(\frac{1}{k-1} \sum\limits_{j=1}^k(\overline{X}_{j} - \overline{X})^2 \cdot n_j\right)
= \frac{1}{k-1} \left[ E\left(\sum\limits_{j=1}^k(\overline{X}_{j} - \overline{X})^2 \cdot n_j\right)\right] \stackrel{\color{lightgreen}{по\ доказанному}}{=}
\frac{1}{k-1} \left[ E\left(\sum\limits_{j=1}^k(\overline{X}_{j} - \mu)^2 \cdot n_j\right) - n(\overline X - \mu)^2\right]
= \frac{1}{k-1} \left[ \sum\limits_{j=1}^k\left(n_j\cdot E[(\overline{X}_j - \mu)^2]\right) - n \cdot E[(\overline{X} - \mu)^2]\right]
= \frac{1}{k-1} \left[ \sum\limits_{j=1}^kn_j\cdot \left(Var(\overline{X}_j - \mu) + [E(\overline{X}_j - \mu)]^2\right) - n \cdot \left(Var(\overline{X}) + (\mu - \mu)^2\right)\right]
= \frac{1}{k-1} \left[ \sum\limits_{j=1}^kn_j\cdot \left(Var(\overline{X}_j) + (\mu_j - \mu)^2\right) - n \frac{\sigma^2}{n}\right]
= \frac{1}{k-1} \left[ \sum\limits_{j=1}^k(n_j\cdot \frac{\sigma^2}{n_j} + n_j\cdot(\mu_j - \mu)^2) - \sigma^2\right]
= \frac{1}{k-1} \left[ \sum\limits_{j=1}^k(n_j\cdot(\mu_j - \mu)^2) + k \sigma^2 - \sigma^2\right]
$<br>$
= \frac{1}{k-1} \left[ \sum\limits_{j=1}^k(n_j\cdot(\mu_j - \mu)^2) + \sigma^2 (k-1)\right]
= \sigma^2 + \frac{1}{k-1} \sum\limits_{j=1}^kn_j\cdot(\mu_j - \mu)^2
$

<hr>'''),
        },
        "Q2": {
            1:
                (r'''Опишите общую схему проверки статистических гипотез. Определите понятия: критическая область, уровень значимости, мощность критерия. Какие гипотезы называются простыми (сложными)?''',
                 r'''**Общая схема проверки статистических гипотез**

1) Выдвижение основной и альтернативной статистических гипотез. Выбор подходящего уровня значимости.

2) Нахождение критических точек и построение критической области.

3) Использование различных статистических критерией для подтверждения или опровержения выдвинутых гипотез, путём проверки вхождения полученного значения в критическую область

4) Принять или опровергнуть нулевую гипотезу

**Критическая область**

Статистическим критерием и критической областью $ K \subset R^{n} $ называется правило, в соотвествии с которым основная гипотеза $ H_0 $ отвергается, если выборка "попадает" в критическую область K, т.е. $ (X_1, X_2, ..., X_n) \in K$, не отвергается, если $ (X_1, X_2, ..., X_n) \notin K$

**Уровень значимости**

Вероятность ошибки первого рода называется уровнем значимости критерия и обозначается через $\alpha$.

**Мощность критерия**

Вероятность ошибки второго рода обозначается через β, а величина W = 1 − $\beta$ называется мощностью критерия.

**Какие гипотезы называются простыми(сложными)**

Гипотеза о значениях параметра $\theta$ называется простой, если она имеет вид $\theta = \theta_0$, $\theta_0$ - фиксированное значение параметра. Гипотеза вида $\theta \in \Theta $, где $ \Theta $ - множество, называется сложной.

<hr>'''),
            2:
                (r'''Приведите вероятностную интерпретацию ошибок первого и второго рода, а также мощности критерия в случае простых нулевой и альтернативной гипотез. Привести пример критерия с выбором критического значения $c_0$, для которого сумма ошибок первого и второго рода $\alpha + \beta$ была бы минимальной.''',
                 r'''1. **Уровень значимости $ \alpha $ означает
вероятность ошибки первого рода, т.е. вероятность отвергнуть верную гипотезу H0**.
<br>
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K)=
P_{H_0}(T(X_1, X_1, . . . , X_n) > c_{\alpha})$, где T - критерий, а $c_{\alpha}$ - критическое значение, K в этой записи правосторонняя

<br>

2. **$ \beta $ означает
вероятность ошибки второго рода, т.е. вероятность отвергнуть верную гипотезу H1**.
<br>
$ \beta = P_{H_1}((X_1, X_1, . . . , X_n) \notin K)= P_{H_1}(T(X_1, X_1, . . . , X_n) < c_{\alpha})$, где T - критерий, а $c_{\alpha}$ - критическое значение, K в этой записи левосторонняя

<br>

3. **Мощность критерия W** (для заданного уровня значимости $\alpha$) определяется так:
<br>
$ W = 1 − \beta = P_{H_1}(T(X_1, X_1, . . . , X_n) > c_{\alpha})$

<br>

**Пример**

Дана выборка из $\mathcal{N}(\mu, \sigma^2)$, дисперсия известна, мат. ожидание - нет.
<br>
Имеются для гипотезы:
<br>
$H_0: \mu = \mu_0; $
<br>
$ H_1: \mu = \mu_1$, где $\mu_1 > \mu_0$

Статистический критерий имеет вид: $ Z = \frac{\overline{X} - \mu_0}{\frac{\sigma}{\sqrt{n}}}$
<br>
Критическое значение $c_{\alpha} = \mu_0 + \frac{\sigma}{\sqrt{n}} \cdot z_{\alpha}$

<br>

![image.png](data:image/png;base64,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Rb5srmdBvnvqOY5gpQtWcMgIRt/77Wd2yinJA7kFVtnomDINHhew6gMrOGBDcQR+pwtLSXkwlb3TTmYLFoT7VayLIGTKMWhjsKT8aaeZfeMb4T5209CbLwluY/YDBiQPREC0l2rzGUXck9n5l14K9198MYwSf523SQicJwr86qvhPia7225h4LwlwGaQHRuKI4ryErZZYw8uDhliduml5pb8aQjY2S67mP32t2ann252zTWh35o7N2spOvhM3joaR2A7faT7uPodwAvG4opC2U1LI/LNtjhyhnnXOTnBEOb/dvBkK9M2cc0AWtJQQl2Og9wfXnrSbiVAd7xnOapDkhQby5sjt27xYiv/8kur/HKR+7zRFkVxcfJDbsGnCMURdbId/1R6VsCiwhBT/mbhN3gLFysa1KNnT7PrrgsZJ7/3/PMhKfnNb5IXNA6qcpHMkdlxyGNjYvMSGlIf0pmv36JNAXH87CopEvjNhkCfm870iafwuw884FbTsnnzwpl5xgL+PGkSf/97KCPnIcdkjETR0maF30F2bKjdQEVROA8UgV9pCFyjSqmS31lEnklqZaHU6D0hnI2RYRZk33prFs8O96mI730vHM1kifBV1oVtN47AdljSkb9xxdLq+HIGlvdrqc9vNhkmt5hIcdccym3MJqrUMOOazA/WNtIh5TJwh6wX226OhVzeY44xU+fiQJQEMkIv3BBmzHAkpejii61AmyMs0Y2ITBQ5GkVA9+TAxRHYDp1qqxMabODWW82mTTP3Tm6SXsnlbWWEfieFEPToETI82Oxrr5ldconZ/vsnTzYMeBBmN3NmmKv761/zgqTkyQyYPz/k36nm6zeChe+xtERSxZixN2XsprIR3WcyeyZLBg82Gz/e7Oyzw3TVK680+1byzc8HHBBGg885x+zMM0PSfOGFZqnPbLe0WTnbkeztRsfWrzf7+c/Deva45Raz225L7mTAp5+6SilQ5XSdKNtIrTDygyHJUTSmJM77KC31SYXvvntIhrOEGgti63eQmvXM4yl9iLUsQh5TIHltC5XfbDJMusT/DxFhDx7AKeHtATEFL0yIK9A6a02225QThIMIzWabhft8JiJHdMQDp00UI+q86c3VedXcfLPV3nJz2JFFtxtuSF6Y2+iWnxeLBxfTAdvhzXOtajuQlClTwrDqqFFhtIw5e1gl9e+3TOBd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)

Включаем воображение: есть 2 графика плотности нормального распределения. Левый - когда верна $H_0$, правый когда верна $H_1$. По оси x $\mu$ и $c_{\alpha}$. Правее от $c_{\alpha}$ площадь левого распределения это $\alpha$, зеркально также $\beta$
<br>
Из графика наглядно видно, что при таких гипотезах данный критерий будет иметь наименьщую сумму ошибок 1 и 2 рода при $c_{\alpha}$, равноудалённым от вершин плотностей данных распределений, то есть в точке, где плотности равны друг другу.. Если взять точку правее оговорённой, то производная второго графика по модулю больше, чем у первого(тоже по модулю), то есть $\beta$ прирастает быстрее, чем убывает $\alpha$. Точка левее аналогично. Итог: $c_{\alpha} = \frac{\mu_0 + \mu_1}{2}$

<hr>'''),
            3:
                (r'''Дайте определение несмещенности и состоятельности критерия. Пусть мощность критерия определяется выражением $W(\mu) = \frac {1}{2} - Φ_0(z_α - \frac {\sqrt n}{\sigma} (\mu - \mu_0)), \mu \in \Theta_1 = (\mu_0; +\infty)$. Является ли критерий с такой функцией мощности несмещенным и состоятельным? Ответ обосновать.''',
                 r'''Если $W(\theta) \geq \alpha$ для $\forall \theta \in \Theta_{1} (W $- мощность статистического критерия), то статистический критерий называется <b>несмещённым</b>
<br>
Если для $\forall \theta  \in \Theta_{1} $ функция мощности $W(\theta) \xrightarrow[n\to+\infty]{} 1$, то статистический критерий называется <b>состоятельным</b>

$W(\mu_1) = 1 - \beta = P_{H_1}(\overline{X} > c_\alpha) = \frac{1}{2} - \Phi_0(z_{\alpha} - \frac{\sqrt{n}}{\sigma}(\mu_1 - \mu_0))$
<br>
Необходимо показать, что $W(\theta) \geq \alpha$
<br>
1. $\Phi_0$ - неубывающая функция, следовательно $-\Phi_0$ невозрастающая. Рассмотрим её минимальное значение. Это случай, когда $\mu = \mu_0$ (так как $\mu_1 >= \mu_0$), тогда:
<br>
$W = \frac{1}{2} - \Phi_0(z_\alpha - \frac{\sqrt{n}}{\sigma}\cdot 0) = \frac{1}{2} - \Phi_0(z_\alpha) = \frac12 - (F(z_\alpha) - \frac12) = 1 - P(Z \leq z_\alpha) = 1 - 1 + P(Z > z_\alpha) = \alpha$
<br>
Но так как $\mu_1 > \mu_0$, a $\Phi_0$ - неубывающая функция, то $W(\theta) \geq \alpha \Longrightarrow$ критерий несмещенный
<br>
2. при $n\to\infty$
<br>
$W = \frac{1}{2} - \Phi_0(z_\alpha - \infty) = \frac{1}{2} - (F(-\infty) - \frac{1}{2}) = \frac{1}{2} - 0 + \frac{1}{2} = 1 \Longrightarrow$ критерий состоятельный

<hr>'''),
            4:
                (r'''Сформулируйте лемму Неймана-Пирсона в случае проверки двух простых гипотез. Приведите пример построения наиболее мощного критерия.''',
                 r'''**Лемма Неймана-Пирсона**

Наиболее мощный критерий для проверки простой гипотезы $H_0$ против простой альтернативно гипотезы $H_1$ с вероятностью ошибки первого рода $\alpha$ существует и задаётся критической областью вида $K_{\alpha} = \{\overrightarrow{x} = (x_1, x_2, ..., x_n): T(\overrightarrow{x}) = \frac{\prod\limits_{k = 1}^n f(x_k, \theta_1)}{\prod\limits_{k = 1}^n f(x_k, \theta_0)} > c_{\alpha}\}$, где $c_{\alpha}$ из условия $P_{H_0}(T(\overrightarrow{X})> c_{\alpha}) = \alpha$, $\overrightarrow{X}$ - случайная выборка, $\overrightarrow{x}$ - её реализация

<br>

**Пример**

Дана выборка из $\mathcal{N}(\mu, \sigma^2)$, $\sigma^2 = Var(X) $ известна, $ \theta = \mu = E(X) $ - неизвестно.
<br>
Имеются для гипотезы:

$H_0: \mu = \mu_0; $
<br>
$ H_1: \mu = \mu_1$, где $\mu_1 > \mu_0$

<br>

$\large T(\overrightarrow{x}) = \frac{\prod\limits_{k = 1}^n f(x_k, \theta_1)}{\prod\limits_{k = 1}^n f(x_k, \theta_0)}
= \frac{
\frac{1}{\sigma\sqrt{2\pi}}
e^{-\frac{1}{2\sigma^2}
\sum\limits_{k=1}^n(x_k - \mu_1)^2
}}
{\frac{1}{\sigma\sqrt{2\pi}}
e^{-\frac{1}{2\sigma^2}
\sum\limits_{k=1}^n(x_k - \mu_0)^2
}}
=
e^{-\frac{1}{2\sigma^2}
\sum\limits_{k=1}^n[(x_k - \mu_1)^2 - (x_k - \mu_0)^2]
}
= e^{-\frac{1}{2\sigma^2}
\sum\limits_{k=1}^n[x_k^2 - 2 x_k \mu_1 + \mu_1^2 - x_k^2 + 2 x_k \mu_0 - \mu_0^2]}
=
e^{-\frac{1}{2\sigma^2}
\sum\limits_{k=1}^n[2 x_k (\mu_0 - \mu_1) + \mu_1^2  - \mu_0^2]}
=
e^{\frac{n}{\sigma^2}(\mu_1 - \mu_0)\overline{x}
-
\frac{n}{2\sigma^2}(\mu_1^2 - \mu_0^2)}
$

<br>

Из $K_{\alpha} = \{\overrightarrow{x} = (x_1, x_2, ..., x_n): T(\overrightarrow{x}) > c_{\alpha}) $ получим:

$ \overline{x} > \frac{\sigma^2}{n(\mu_1 - \mu_0)} \ln{c} + \frac{\mu_1 + \mu_0}{2}$

В общем случае $K_{\alpha} = \{(x_1, x_2, ..., x_n): \overline{x} > c_{\alpha}\} $, где $ {c_{\alpha} = \mu_0 + \frac{\sigma}{\sqrt{n}}} \cdot z_{\alpha} $

Получим следующее уравнение:

$\frac{\sigma^2}{n(\mu_1 - \mu_0)} \ln{c} + \frac{\mu_1 + \mu_0}{2} = c_{\alpha} = \mu_0 + \frac{\sigma}{\sqrt{n}} \cdot z_{\alpha}$

Откуда
$ c =
e^{-(\mu_1 - \mu_0)
[\frac{n}{2\sigma^2}(\mu_1 - \mu_0) - \frac{\sqrt{n}}{\sigma}z_{\alpha}]
} $

<br>

Таким образом, наиболее мощный критерий имеет следующую критическую область: $K_{\alpha} = \{\overrightarrow{x} = (x_1, x_2, ..., x_n): T(\overrightarrow{x}) > e^{-(\mu_1 - \mu_0)
[\frac{n}{2\sigma^2}(\mu_1 - \mu_0) - \frac{\sqrt{n}}{\sigma}z_{\alpha}]
}) $, где T - статистика отношения правдоподобия

<hr>'''),
            5:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\sigma^2 = Var(X)$ – **известна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu = \mu_0$ против альтернативной гипотезы $H_1 : \mu > \mu_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.

Пусть  Var(X) известна, а параметр $\mu$  неизвестен, и пусть $X_1, X_2,...,X_n$ - выборка объема n  из этого распределения.
- Основная гипотеза $H_0: \mu=\mu_0$
- Альтернативная гипотеза $H_0: \mu>\mu_0$''',
                 r'''Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{Z = \frac{(\overline{X} - \mu_0)\sqrt{n}}{\sigma}}$

Критическая область
$\color{orange}{K_{\alpha} = \{z_{\alpha}, +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ Z \sim \mathcal{N}(0; 1)}$
<br>
При выполнении нулевой гипотезы, математическое ожидание рассматриваемого распределения будет равно $ \mu_0 $. В таком случае Z статистика примет значение равное $ \frac{\sqrt{n}(\mu_0 - \mu_0)}{\sigma} $ = 0, а следовательно и математическое ожидание статистики будет равно 0.
<br>
Найдём дисперсию Z статистики:
$ Var(Z) = Var(\frac{\sqrt{n}(\overline{X} - \mu_0)}{\sigma}) = \frac{nVar(\overline{X} - \mu_0)}{\sigma^2}
= \frac{n(Var(\overline{X}) + 0)}{\sigma^2} = \frac{n(\frac{\sigma^2}{n})}{\sigma^2} = 1$
<br>
Z является нормальным распределнием, исходя из центральной предельной теоремы. Она имеет математическое ожидание, равное 0 и дисперсию, равную 1, а следовательно является стандартным нормальным распределением.


2. $\color{orange}{Критерий,\ основанный\ на\ статистике\ Z,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(Z > z_{\alpha})$
<br>
Мы знаем, что Z является стандартным нормальным распределением при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению. Также по определению она равна $\alpha$.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. То есть это вероятность, что $ P(Z < z_{\alpha}| \mu=\mu_1) = P(Z + \frac{\sqrt{n}(\mu_1 - \mu_0)}{\sigma} < z_{\alpha}) = P(Z < z_{\alpha} - \frac{\sqrt{n}(\mu_1 - \mu_0)}{\sigma}) = \frac{1}{2}+\Phi(z_{\alpha} - \frac{\sqrt{n}(\mu_1 - \mu_0)}{\sigma})$. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Наша критическая область является правосторонней, что обусловлено выбором вида альтернативной гипотезы. В таком случае, pv значение будет являться вероятностью получить большее значение, чем значение наблюдаемой статистики критерия.
<br>
$\color{orange}{pv = P_{H_0}(Z(\overrightarrow{X}) > Z(\overrightarrow{x})) = P_{H_0}(Z > z_{стат}) = 1 - P_{H_0}(Z \leq z_{стат}) = 1 - F_Z(z_{стат}) = \frac{1}{2} - \Phi_0(z_{стат})}$.
<br>
Это можно интерпретировать так: если pv высоко, то значение критерия достаточно низко, чтобы не войти в $K_{\alpha}$. Если это значение выше, чем какой-то изначально установленный уровень вероятности ошибки первого рода, то есть значение $\alpha$, то мы можем удтверждать, что выбранный критерий обеспечивает необходимый уровень значимость, а значит гипотеза $H_0$ принимается.

<hr>'''),
            6: (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\sigma^2 = Var(X)$ – **известна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu = \mu_0$ против альтернативной гипотезы $H_1 : \mu < \mu_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                r'''1)
Статистика
$\color{orange}{Z = \frac{\sqrt{n}(\overline{X} - \mu_0)}{\sigma}}$
<br>
Критическая область
$\color{orange}{K_{\alpha} = \{-\infty, -z_{\alpha}\}}$
<br>
2)
Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ Z \sim \mathcal{N}(0; 1)}$
<br>
При выполнении нулевой гипотезы, математическое ожидание рассматриваемого распределения будет равно $ \mu_0 $. В таком случае Z статистика примет значение равное $ \frac{\sqrt{n}(\mu_0 - \mu_0)}{\sigma} $ = 0, а следовательно и математическое ожидание статистики будет равно 0.
<br>
Найдём дисперсию Z статистики:
$ Var(Z) = Var(\frac{\sqrt{n}(\overline{X} - \mu_0)}{\sigma}) = \frac{nVar(\overline{X} - \mu_0)}{\sigma^2}
= \frac{n(Var(\overline{X}) + 0)}{\sigma^2} = \frac{n(\frac{\sigma^2}{n})}{\sigma^2} = 1$
Z является нормальным распределнием, исходя из центральной предельной теоремы. Она имеет математическое ожидание, равное 0 и дисперсию, равную 1, а следовательно является стандартным нормальным распределением.


2. $\color{orange}{Критерий,\ основанный\ на\ статистике\ Z,\ имеет\ уровень\
значимости\ \alpha }$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(Z < -z_{\alpha})$
<br>
Мы знаем, что Z является стандартным нормальным распределением при выполнении $H_0$, а следовательно данная вероятность это квантиль этого распределения в точке $\alpha$ по определению. Также по определению она равна $\alpha$


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. То есть это вероятность, что $ P(Z > -z_{\alpha}| \mu=\mu_1) = P(Z + \frac{\sqrt{n}(\mu_1 - \mu_0)}{\sigma} > -z_{\alpha}) = 1 - P(Z \leq -z_{\alpha} - \frac{\sqrt{n}(\mu_1 - \mu_0)}{\sigma}) = \frac{1}{2} - \Phi(-z_{\alpha} - \frac{\sqrt{n}(\mu_1 - \mu_0)}{\sigma})= \frac{1}{2} + \Phi(z_{\alpha} - \frac{\sqrt{n}(\mu_0 - \mu_1)}{\sigma})$.
<br>
Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Наша критическая область является левосторонней, что обусловлено выбором вида альтернативной гипотезы. В таком случае, pv значение будет являться вероятностью получить меньшее значение, чем значение наблюдаемой статистики критерия.
<br>
$\color{orange}{pv = P_{H_0}(Z(\overrightarrow{X}) < Z(\overrightarrow{x})) = P_{H_0}(Z < z_{стат}) = F_Z(z_{стат}) = \frac{1}{2} + \Phi_0(z_{стат})}$.
<br>
Это можно интерпретировать так: если pv высоко, то значение критерия достаточно высоко, чтобы не войти в $K_{\alpha}$. Если это значение выше, чем какой-то изначально установленный уровень вероятности ошибки первого рода, то есть значение $\alpha$, то мы можем удтверждать, что выбранный критерий обеспечивает необходимый уровень значимость, а значит гипотеза $H_0$ принимается.

<hr>'''),
            7: (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\sigma^2 = Var(X)$ – **известна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu = \mu_0$ против альтернативной гипотезы $H_1 : \mu \neq \mu_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                r'''1)
Статистика
$\color{orange}{Z = \frac{\sqrt{n}(\overline{X} - \mu_0)}{\sigma}}$
<br>
Критическая область
$\color{orange}{K_{\alpha} = \{(-\infty, -z_{\frac{\alpha}{2}}) \cup (z_{\frac{\alpha}{2}}, \infty\})}$
<br>
2)
Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ Z \sim \mathcal{N}(0; 1)}$
<br>
При выполнении нулевой гипотезы, математическое ожидание рассматриваемого распределения будет равно $ \mu_0 $. В таком случае Z статистика примет значение равное $ \frac{\sqrt{n}(\mu_0 - \mu_0)}{\sigma} $ = 0, а следовательно и математическое ожидание статистики будет равно 0.
<br>
Найдём дисперсию Z статистики:
$ Var(Z) = Var(\frac{\sqrt{n}(\overline{X} - \mu_0)}{\sigma}) = \frac{nVar(\overline{X} - \mu_0)}{\sigma^2}
= \frac{n(Var(\overline{X}) + 0)}{\sigma^2} = \frac{n(\frac{\sigma^2}{n})}{\sigma^2} = 1$
<br>
Z является нормальным распределнием, исходя из центральной предельной теоремы. Она имеет математическое ожидание, равное 0 и дисперсию, равную 1, а следовательно является стандартным нормальным распределением.


2. $\color{orange}{Критерий,\ основанный\ на\ статистике\ Z,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(Z < -z_{\frac{\alpha}{2}}| Z > z_{\frac{\alpha}{2}}) =
P_{H_0}(Z < -z_{\frac{\alpha}{2}}) + P_{H_0}(Z > z_{\frac{\alpha}{2}})$
<br>
Мы знаем, что Z является стандартным нормальным распределением при выполнении $H_0$, а следовательно данные вероятности это квантиль и верхняя процентная точка этого распределения в точке $\frac{\alpha}{2}$ по определению. Также по определению обе вероятности равны $\frac{\alpha}{2}$, а в сумме они дают $\alpha$


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. То есть это вероятность, что $ P(Z < z_{\frac{\alpha}{2}}| \mu=\mu) - P(Z < -z_{\frac{\alpha}{2}}| \mu=\mu) = P(Z + \frac{\sqrt{n}(\mu - \mu_0)}{\sigma} < z_{\frac{\alpha}{2}}) - P(Z + \frac{\sqrt{n}(\mu - \mu_0)}{\sigma} < -z_{\frac{\alpha}{2}}) = P(Z < z_{\frac{\alpha}{2}} - \frac{\sqrt{n}(\mu - \mu_0)}{\sigma}) + 1 - P(Z \leq -z_{\frac{\alpha}{2}} - \frac{\sqrt{n}(\mu - \mu_0)}{\sigma}) = \frac{1}{2}+\Phi(z_{\frac{\alpha}{2}} - \frac{\sqrt{n}(\mu - \mu_0)}{\sigma}) - \frac{1}{2} - \Phi(-z_{\frac{\alpha}{2}} - \frac{\sqrt{n}(\mu - \mu_0)}{\sigma}) = \Phi(z_{\frac{\alpha}{2}} - \frac{\sqrt{n}(\mu - \mu_0)}{\sigma}) + \Phi(z_{\frac{\alpha}{2}} + \frac{\sqrt{n}(\mu - \mu_0)}{\sigma})$
<br>
Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Наша критическая область является двусторонней, что обусловлено выбором вида альтернативной гипотезы. В таком случае, pv значение будет являться удвоенным минимумом из pv значений предыдущих двух пунктов. Это верно, потому что рассматривая двустороннюю область, ошибка первого рода может появиться как при превыщающих, так и при меньших значениях критерия. Это, опять же, связано с видом альтернативной гипотезы. Как мы рассмотрели ранее, вероятность ошибки первого рода при рассмотрении двух хвостов с ${\frac{\alpha}{2}}$ эквивалентна вероятности одного хвоста распределения с ${\alpha}$. Тогда, хвост, имеющий меньшее pv значение, приводит к большему основанию об отклонении нулевой гипотезы, поэтому мы рассматриваем именно его. Умножение на двойку в формуле возникает для стандартизации двустороннего вида и одностороннего, ведь без этой двойки для вывода об отклонении или принятии гипотезы, пришлось бы сравнивать с ${\frac{\alpha}{2}}$ вместо ${\alpha}$, а благодаря этому, мы также работаем с просто ${\alpha}$.
<br>
$\color{orange}{PV = 2min\{p_1, p_2\} = P_{H_0}(|Z(\vec{X})| > |Z(\vec{x})|) = P_{H_0}(|Z| > |z_{стат}|) = P_{H_0}(Z < -|z_{стат}|) + P_{H_0}(Z > |z_{стат}|) = F_Z(-|z_{стат}|) + 1 - F_Z(|z_{стат}|) = \frac{1}{2} - \Phi_0(|z_{стат}|) + 1 - \frac{1}{2} - \Phi_0(|z_{стат}|) = 1 - 2\Phi_0(|z_{стат}|)}$

<hr>'''),
            8:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\sigma^2 = Var(X)$ – **неизвестна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu = \mu_0$ против альтернативной гипотезы $H_1 : \mu > \mu_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  неизвестен, и пусть $X_1, X_2,...,X_n$ - выборка объема n  из этого распределения.
- Основная гипотеза $H_0: \mu=\mu_0$
- Альтернативная гипотеза $H_0: \mu>\mu_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{T = \frac{(\overline{X} - \mu_0)\sqrt{n}}{s}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{t_{\alpha}(n-1), +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ T \sim \mathcal{t}(n - 1)}$
<br>
При выполнении нулевой гипотезы, оценка, используемая для замены неизвестного стандартного отклонения, будет равна $\sqrt{\frac{n}{n-1}}\sigma$.
<br>
Подставив найдённое значение в формулу T-критерия получим:
$T = \frac{(\overline{X} - \mu_0)\sqrt{n}\sqrt{n-1}}{\sqrt{n}\sigma} = \frac{(\overline{X} - \mu_0)\sqrt{n-1}}{\sigma}$, что равно распределению Стьюдента с n-1 степенью свободы по определению.


2. $\color{orange}{Критерий,\ основанный\ на\ T\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(T > t(n-1)_{\alpha})$
<br>
Мы знаем, что T является распределением стьюдента с n-1 степенью свободы при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению. Также по определению она равна $\alpha$


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = G_{n-1, \delta}(t_{\alpha}(n-1))$, где G - нецентральное распределение Стьюдента. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Наша критическая область является правосторонней, что обусловлено выбором вида альтернативной гипотезы. В таком случае, pv значение будет являться вероятностью получить большее значение, чем значение наблюдаемой статистики критерия.
<br>
$\color{orange}{pv = P_{H_0}(T(\overrightarrow{X}) > T(\overrightarrow{x})) = P_{H_0}(T > t_{стат}) = 1-t_{n-1}(t_{стат})}$.
<br>
Это можно интерпретировать так: если pv высоко, то значение критерия достаточно низко, чтобы не войти в $K_{\alpha}$. Если это значение выше, чем какой-то изначально установленный уровень вероятности ошибки первого рода, то есть значение $\alpha$, то мы можем удтверждать, что выбранный критерий обеспечивает необходимый уровень значимость, а значит гипотеза $H_0$ принимается.

<hr>'''),
            9:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\sigma^2 = Var(X)$ – **неизвестна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu = \mu_0$ против альтернативной гипотезы $H_1 : \mu < \mu_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  неизвестен, и пусть $X_1, X_2,...,X_n$ - выборка объема n  из этого распределения.
- Основная гипотеза $H_0: \mu=\mu_0$
- Альтернативная гипотеза $H_0: \mu<\mu_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{T = \frac{(\overline{X} - \mu_0)\sqrt{n}}{s}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{-\infty; -t_\alpha(n-1)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ T \sim \mathcal{t}(n - 1)}$
<br>
При выполнении нулевой гипотезы, оценка, используемая для замены неизвестного стандартного отклонения, будет равна $\sqrt{\frac{n}{n-1}}\sigma$.
<br>
Подставив найдённое значение в формулу T-критерия получим:
$T = \frac{(\overline{X} - \mu_0)\sqrt{n}\sqrt{n-1}}{\sqrt{n}\sigma} = \frac{(\overline{X} - \mu_0)\sqrt{n-1}}{\sigma}$, что равно распределению Стьюдента с n-1 степенью свободы по определению.


2. $\color{orange}{Критерий,\ основанный\ на\ T\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(T < -t(n-1)_{\alpha}) = 1 - P_{H_0}(T > t(n-1)_{1 - \alpha}) = 1 - 1 + \alpha$
<br>
Мы знаем, что T является распределением стьюдента с n-1 степенью свободы при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $1 - \alpha$ по определению. Также по определению она равна $1 - 1 + \alpha = \alpha$


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = 1 - G_{n-1, \delta}(-t_{\alpha}(n-1))$, где G - нецентральное распределение Стьюдента. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Наша критическая область является левосторонней, что обусловлено выбором вида альтернативной гипотезы. В таком случае, pv значение будет являться вероятностью получить меньшее значение, чем значение наблюдаемой статистики критерия.
<br>
$\color{orange}{pv = P_{H_0}(T(\overrightarrow{X}) < T(\overrightarrow{x})) = P_{H_0}(T < t_{стат}) = t_{n-1}(t_{стат})}$.
<br>
Это можно интерпретировать так: если pv высоко, то значение критерия достаточно высоко, чтобы не войти в $K_{\alpha}$. Если это значение выше, чем какой-то изначально установленный уровень вероятности ошибки первого рода, то есть значение $\alpha$, то мы можем удтверждать, что выбранный критерий обеспечивает необходимый уровень значимость, а значит гипотеза $H_0$ принимается.

<hr>'''),
            10:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\sigma^2 = Var(X)$ – **неизвестна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu = \mu_0$ против альтернативной гипотезы $H_1 : \mu \neq \mu_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  неизвестен, и пусть $X_1, X_2,...,X_n$ - выборка объема n  из этого распределения.
- Основная гипотеза $H_0: \mu=\mu_0$
- Альтернативная гипотеза $H_0: \mu\neq\mu_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{T = \frac{(\overline{X} - \mu_0)\sqrt{n}}{s}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\left(-\infty; -t_{\frac{\alpha}{2}}(n-1)\right) \cup \left(t_{\frac{\alpha}{2}}(n-1); +\infty\right)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ T \sim \mathcal{t}(n - 1)}$
<br>
При выполнении нулевой гипотезы, оценка, используемая для замены неизвестного стандартного отклонения, будет равна $\sqrt{\frac{n}{n-1}}\sigma$.
<br>
Подставив найдённое значение в формулу T-критерия получим:
$T = \frac{(\overline{X} - \mu_0)\sqrt{n}\sqrt{n-1}}{\sqrt{n}\sigma} = \frac{(\overline{X} - \mu_0)\sqrt{n-1}}{\sigma}$, что равно распределению Стьюдента с n-1 степенью свободы по определению.


2. $\color{orange}{Критерий,\ основанный\ на\ T\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(T > t(n-1)_{\frac{\alpha}{2}}) + P_{H_0}(T < -t(n-1)_{\frac{\alpha}{2}}) = \frac{\alpha}{2} + 1 - P_{H_0}(T > t(n-1)_{1 - \frac{\alpha}{2}}) = \alpha$
<br>
Мы знаем, что T является распределением стьюдента с n-1 степенью свободы при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\frac{\alpha}{2}$ по определению. Также их сумма равна $\alpha$.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = G_{n-1, \delta}(t_{\frac{\alpha}{2}}(n-1)) - G_{n-1, \delta}(-t_{\frac{\alpha}{2}}(n-1))$, где G - нецентральное распределение Стьюдента. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Наша критическая область является двусторонней, что обусловлено выбором вида альтернативной гипотезы. В таком случае, pv значение будет являться удвоенным минимумом из pv значений предыдущих двух пунктов. Это верно, потому что рассматривая двустороннюю область, ошибка первого рода может появиться как при превыщающих, так и при меньших значениях критерия. Это, опять же, связано с видом альтернативной гипотезы. Как мы рассмотрели ранее, вероятность ошибки первого рода при рассмотрении двух хвостов с ${\frac{\alpha}{2}}$ эквивалентна вероятности одного хвоста распределения с ${\alpha}$. Тогда, хвост, имеющий меньшее pv значение, приводит к большему основанию об отклонении нулевой гипотезы, поэтому мы рассматриваем именно его. Умножение на двойку в формуле возникает для стандартизации двустороннего вида и одностороннего, ведь без этой двойки для вывода об отклонении или принятии гипотезы, пришлось бы сравнивать с ${\frac{\alpha}{2}}$ вместо ${\alpha}$, а благодаря этому, мы также работаем с просто ${\alpha}$.
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1, p_2\} = P_{H_0}(|T(\vec{X})| > |T(\vec{x})|) = P_{H_0}(T < -|t_{стат}|) + P_{H_0}(T > |t_{стат}|) = 1 - P_{H_0}(T < |t_{стат}|) + 1 - P_{H_0}(T < |t_{стат}|) = 2 - 2t_{n-1}(|t_{стат}|)}$

<hr>'''),
            11:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\mu = E(X)$ – **известна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma = \sigma_0$ против альтернативной гипотезы $H_1 : \sigma > \sigma_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  известен, и пусть $X_1, X_2,...,X_n$ - выборка объема n из этого распределения.
- Основная гипотеза $H_0: \sigma=\sigma_0$
- Альтернативная гипотеза $H_0: \sigma > \sigma_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{\chi^2_0 = \frac{ns^2_0}{\sigma^2_0}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\chi^2_\alpha(n); +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \chi^2_0 \sim \chi^2(n)}$
<br>
При выполнении нулевой гипотезы, $\sigma = \sigma_0$.
<br>
$\chi^2_0 = \frac{ns^2_0}{\sigma^2_0} = \frac{1}{\sigma^2}\sum_{i=1}^{n} (X_i - \mu)^2 = \sum_{i=1}^{n} (\frac{X_i - \mu}{\sigma})^2 \stackrel{\color{lightgreen}{Z = \frac{X - \mu}{\sigma}}}{=} \sum_{i=1}^{n} Z_i^2 = \chi^2(n)$.


2. $\color{orange}{Критерий,\ основанный\ на\ \chi^2_0\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\chi^2_0 > \chi^2_\alpha(n)) = \alpha$
<br>
Мы знаем, что $\chi^2_0$ является распределением $\chi^2(n)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = F_{\chi^2_n}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_\alpha(n)\right)$, где $F_{\chi^2_n}(\cdot)$ - функция распределения хи-квадрат. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(T(\vec{X}) > T(\vec{x})) = P_{H_0}(\chi^2 > \chi^2_{стат}) = 1 - P_{H_0}(\chi^2 < \chi^2_{стат}) = 1 - \chi^2_n(\chi^2_{стат})}$

<hr>'''),
            12:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\mu = E(X)$ – **известна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma = \sigma_0$ против альтернативной гипотезы $H_1 : \sigma < \sigma_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  известен, и пусть $X_1, X_2,...,X_n$ - выборка объема n из этого распределения.
- Основная гипотеза $H_0: \sigma=\sigma_0$
- Альтернативная гипотеза $H_0: \sigma < \sigma_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{\chi^2_0 = \frac{ns^2_0}{\sigma^2_0}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{0; \chi^2_{1 - \alpha}(n)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \chi^2_0 \sim \chi^2(n)}$
<br>
При выполнении нулевой гипотезы, $\sigma = \sigma_0$.
<br>
$\chi^2_0 = \frac{ns^2_0}{\sigma^2_0} = \frac{1}{\sigma^2}\sum_{i=1}^{n} (X_i - \mu)^2 = \sum_{i=1}^{n} (\frac{X_i - \mu}{\sigma})^2 \stackrel{\color{lightgreen}{Z = \frac{X - \mu}{\sigma}}}{=} \sum_{i=1}^{n} Z_i^2 = \chi^2(n)$.


2. $\color{orange}{Критерий,\ основанный\ на\ \chi^2_0\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\chi^2_0 < \chi^2_{1-\alpha}(n)) = 1 - P_{H_0}(\chi^2_0 > \chi^2_{1-\alpha}(n)) = 1 - 1 + \alpha = \alpha$
<br>
Мы знаем, что $\chi^2_0$ является распределением $\chi^2(n)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = 1 - F_{\chi^2_n}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_{1-\alpha}(n)\right)$, где $F_{\chi^2_n}(\cdot)$ - функция распределения хи-квадрат. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(T(\vec{X}) < T(\vec{x})) = P_{H_0}(\chi^2 < \chi^2_{стат}) = \chi^2_n(\chi^2_{стат})}$

<hr>'''),
            13:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\mu = E(X)$ – **известна**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma = \sigma_0$ против альтернативной гипотезы $H_1 : \sigma \neq \sigma_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  известен, и пусть $X_1, X_2,...,X_n$ - выборка объема n из этого распределения.
- Основная гипотеза $H_0: \sigma=\sigma_0$
- Альтернативная гипотеза $H_0: \sigma \neq \sigma_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{\chi^2_0 = \frac{ns^2_0}{\sigma^2_0}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\left(0; \chi^2_{1 - \frac{\alpha}{2}}(n)\right) \cup \left(\chi^2_{\frac{\alpha}{2}}(n); +\infty\right)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \chi^2_0 \sim \chi^2(n)}$
<br>
При выполнении нулевой гипотезы, $\sigma = \sigma_0$.
<br>
$\chi^2_0 = \frac{ns^2_0}{\sigma^2_0} = \frac{1}{\sigma^2}\sum_{i=1}^{n} (X_i - \mu)^2 = \sum_{i=1}^{n} (\frac{X_i - \mu}{\sigma})^2 \stackrel{\color{lightgreen}{Z = \frac{X - \mu}{\sigma}}}{=} \sum_{i=1}^{n} Z_i^2 = \chi^2(n)$.


2. $\color{orange}{Критерий,\ основанный\ на\ \chi^2_0\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\chi^2_0 < \chi^2_{1 - \frac{\alpha}{2}}(n)) + P_{H_0}(\chi^2_0 > \chi^2_{\frac{\alpha}{2}}(n)) = 1 - (1 - \frac{\alpha}{2}) + \frac{\alpha}{2} = \alpha$
<br>
Мы знаем, что $\chi^2_0$ является распределением $\chi^2(n)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\frac{\alpha}{2}$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = F_{\chi^2_n}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_{\frac{\alpha}{2}}(n)\right) - F_{\chi^2_n}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_{1 - \frac{\alpha}{2}}(n)\right)$, где $F_{\chi^2_n}(\cdot)$ - функция распределения хи-квадрат. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1; p_2\} = 2min\{\chi^2_n(\chi^2_{стат}); 1 - \chi^2_n(\chi^2_{стат})\}}$

<hr>'''),
            14:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\mu = \mathbb{E}(X)$ – **неизвестно**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma = \sigma_0$ против альтернативной гипотезы $H_1 : \sigma > \sigma_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна и параметр $\mu$  неизвестен, и пусть $X_1, X_2,...,X_n$ - выборка объема n из этого распределения.
- Основная гипотеза $H_0: \sigma=\sigma_0$
- Альтернативная гипотеза $H_0: \sigma > \sigma_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{\chi^2 = \frac{(n-1)s^2}{\sigma^2}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\chi^2_\alpha(n-1); +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \chi^2 \sim \chi^2(n-1)}$
<br>
При выполнении нулевой гипотезы, $\sigma = \sigma_0$. Докажем преинтересный факт:
<br>
$\sum_{i=1}^{n}{(X_i - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X + \overline X - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X)^2} + 2\sum_{i=1}^{n}{(\overline X - \mu)(X_i - \overline X)} + \sum_{i=1}^{n}{(\overline X - \mu)^2} \stackrel{\color{lightgreen}{\sum (\overline X - \mu) = 0}}{=} \sum_{i=1}^{n}{(X_i - \overline X)^2} + n(\overline X - \mu)$
<br>
<br>
Тогда:
<br>
$\chi^2 = \frac{ns^2}{\sigma^2_0} = \frac{1}{\sigma^2}\sum_{i=1}^{n} (X_i - \overline X)^2 = \stackrel{\color{lightgreen}{по\ доказанному}}{=}
\frac{1}{\sigma^2}\left(\sum_{i=1}^{n} (X_i - \mu)^2 - n(\overline X - \mu)^2\right) = \sum_{i=1}^{n} (\frac{X_i - \mu}{\sigma})^2 - \left(\frac{\sqrt{n}(\overline X - \mu)}{\sigma}\right)^2 \stackrel{\color{lightgreen}{Z = \frac{X - \mu}{\sigma}}}{=}
\sum_{i=1}^{n} Z_i^2 - Z_0^2 =
\sum_{i=1}^{n - 1} Z_i^2 = \chi^2(n-1)$.


2. $\color{orange}{Критерий,\ основанный\ на\ \chi^2\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\chi^2 > \chi^2_\alpha(n-1)) = \alpha$
<br>
Мы знаем, что $\chi^2$ является распределением $\chi^2(n)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = F_{\chi^2_{n-1}}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_\alpha(n-1)\right)$, где $F_{\chi^2_{n-1}}(\cdot)$ - функция распределения хи-квадрат. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(T(\vec{X}) > T(\vec{x})) = P_{H_0}(\chi^2 > \chi^2_{стат}) = 1 - P_{H_0}(\chi^2 < \chi^2_{стат}) = 1 - \chi^2_{n-1}(\chi^2_{стат})}$

<hr>'''),
            15:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\mu = \mathbb{E}(X)$ – **неизвестно**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma = \sigma_0$ против альтернативной гипотезы $H_1 : \sigma < \sigma_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  известен, и пусть $X_1, X_2,...,X_n$ - выборка объема n из этого распределения.
- Основная гипотеза $H_0: \sigma=\sigma_0$
- Альтернативная гипотеза $H_0: \sigma < \sigma_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{\chi^2 = \frac{(n-1)s^2}{\sigma^2_0}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{0; \chi^2_{1 - \alpha}(n-1)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \chi^2 \sim \chi^2(n-1)}$
<br>
При выполнении нулевой гипотезы, $\sigma = \sigma_0$. Докажем преинтересный факт:
<br>
$\sum_{i=1}^{n}{(X_i - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X + \overline X - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X)^2} + 2\sum_{i=1}^{n}{(\overline X - \mu)(X_i - \overline X)} + \sum_{i=1}^{n}{(\overline X - \mu)^2} \stackrel{\color{lightgreen}{\sum (\overline X - \mu) = 0}}{=} \sum_{i=1}^{n}{(X_i - \overline X)^2} + n(\overline X - \mu)$
<br>
<br>
Тогда:
<br>
$\chi^2 = \frac{ns^2}{\sigma^2_0} = \frac{1}{\sigma^2}\sum_{i=1}^{n} (X_i - \overline X)^2 = \stackrel{\color{lightgreen}{по\ доказанному}}{=}
\frac{1}{\sigma^2}\left(\sum_{i=1}^{n} (X_i - \mu)^2 - n(\overline X - \mu)^2\right) = \sum_{i=1}^{n} (\frac{X_i - \mu}{\sigma})^2 - \left(\frac{\sqrt{n}(\overline X - \mu)}{\sigma}\right)^2 \stackrel{\color{lightgreen}{Z = \frac{X - \mu}{\sigma}}}{=}
\sum_{i=1}^{n} Z_i^2 - Z_0^2 =
\sum_{i=1}^{n - 1} Z_i^2 = \chi^2(n-1)$.


2. $\color{orange}{Критерий,\ основанный\ на\ \chi^2\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\chi^2 < \chi^2_{1-\alpha}(n-1)) = 1 - P_{H_0}(\chi^2 > \chi^2_{1-\alpha}(n-1)) = 1 - 1 + \alpha = \alpha$
<br>
Мы знаем, что $\chi^2$ является распределением $\chi^2(n)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = 1 - F_{\chi^2_{n-1}}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_{1-\alpha}(n-1)\right)$, где $F_{\chi^2_{n-1}}(\cdot)$ - функция распределения хи-квадрат. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(T(\vec{X}) < T(\vec{x})) = P_{H_0}(\chi^2 < \chi^2_{стат}) = \chi^2_{n-1}(\chi^2_{стат})}$

<hr>'''),
            16:
                (r'''По выборке $X_1,X_2,...X_n$ объема $n$ из нормального закона распределения $N(\mu;\sigma^2)$, когда $\mu = \mathbb{E}(X)$ – **неизвестно**, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma = \sigma_0$ против альтернативной гипотезы $H_1 : \sigma \neq \sigma_0$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть  Var(X) неизвестна, а параметр $\mu$  известен, и пусть $X_1, X_2,...,X_n$ - выборка объема n из этого распределения.
- Основная гипотеза $H_0: \sigma=\sigma_0$
- Альтернативная гипотеза $H_0: \sigma \neq \sigma_0$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\color{orange}{\chi^2 = \frac{(n-1)s^2}{\sigma^2_0}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\left(0; \chi^2_{1 - \frac{\alpha}{2}}(n-1)\right) \cup \left(\chi^2_{\frac{\alpha}{2}}(n-1); +\infty\right)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \chi^2 \sim \chi^2(n-1)}$
<br>
При выполнении нулевой гипотезы, $\sigma = \sigma_0$. Докажем преинтересный факт:
<br>
$\sum_{i=1}^{n}{(X_i - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X + \overline X - \mu)^2} = \sum_{i=1}^{n}{(X_i - \overline X)^2} + 2\sum_{i=1}^{n}{(\overline X - \mu)(X_i - \overline X)} + \sum_{i=1}^{n}{(\overline X - \mu)^2} \stackrel{\color{lightgreen}{\sum (\overline X - \mu) = 0}}{=} \sum_{i=1}^{n}{(X_i - \overline X)^2} + n(\overline X - \mu)$
<br>
<br>
Тогда:
<br>
$\chi^2_0 = \frac{ns^2}{\sigma^2_0} = \frac{1}{\sigma^2}\sum_{i=1}^{n} (X_i - \overline X)^2 = \stackrel{\color{lightgreen}{по\ доказанному}}{=}
\frac{1}{\sigma^2}\left(\sum_{i=1}^{n} (X_i - \mu)^2 - n(\overline X - \mu)^2\right) = \sum_{i=1}^{n} (\frac{X_i - \mu}{\sigma})^2 - \left(\frac{\sqrt{n}(\overline X - \mu)}{\sigma}\right)^2 \stackrel{\color{lightgreen}{Z = \frac{X - \mu}{\sigma}}}{=}
\sum_{i=1}^{n} Z_i^2 - Z_0^2 =
\sum_{i=1}^{n - 1} Z_i^2 = \chi^2(n-1)$.


2. $\color{orange}{Критерий,\ основанный\ на\ \chi^2_0\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\chi^2_0 < \chi^2_{1 - \frac{\alpha}{2}}(n-1)) + P_{H_0}(\chi^2_0 > \chi^2_{\frac{\alpha}{2}}(n-1)) = 1 - (1 - \frac{\alpha}{2}) + \frac{\alpha}{2} = \alpha$
<br>
Мы знаем, что $\chi^2_0$ является распределением $\chi^2(n)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\frac{\alpha}{2}$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta = F_{\chi^2_{n-1}}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_{\frac{\alpha}{2}}(n-1)\right) - F_{\chi^2_{n-1}}\left(\frac{\sigma^2_0}{\sigma^2}\cdot\chi^2_{1 - \frac{\alpha}{2}}(n-1)\right)$, где $F_{\chi^2_{n-1}}(\cdot)$ - функция распределения хи-квадрат. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1; p_2\} = 2min\{\chi^2_{n-1}(\chi^2_{стат}); 1 - \chi^2_{n-1}(\chi^2_{стат})\}}$

<hr>'''),
            17:
                (r'''По двум независимым выборкам $X_1, X_2, . . . , X_n$ объема n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2, . . . , Y_m$ объема m из $N(\mu_Y; \sigma^2_Y)$, когда $\alpha^2_X = Var(X)$ и $\alpha^2_Y = Var(Y)$ – известны, проверяется на уровне значимости $\alpha$
основная гипотеза $H_0$ : $\mu_X = \mu_Y$ против альтернативной гипотезы $H_1$ : $\mu_X > \mu_Y$ . 1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$. 2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$, причём $Var(X)\ и\ Var(Y)$ - известны.
- Основная гипотеза $H_0: \mu_X=\mu_Y$
- Альтернативная гипотеза $H_0: \mu_X > \mu_Y$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{Z = \frac{\overline X - \overline Y}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{z_\alpha; +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ Z \sim N(0; 1)}$
<br>
При выполнении нулевой гипотезы, $\mu_X = \mu_Y$. Исходя из центральной предельной теоремы, величина $Z$ распределена по нормальному закону.
<br>
$E(Z) = E\left(\frac{\overline X - \overline Y}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}\right) = \frac{E(\overline X) - E(\overline Y)}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}} = \frac{E(X) - E(Y)}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}} \stackrel{\color{lightgreen}{\mu_X = \mu_Y}}{=} 0$.
<br>
$Var(Z) = Var\left(\frac{\overline X - \overline Y}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}\right) = \frac{Var(\overline X) + Var(\overline Y)}{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}} = \frac{{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}{{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}} = 1$
<br>
Получили, что $Z \sim N(0; 1)$


2. $\color{orange}{Критерий,\ основанный\ на\ Z\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(Z > z_\alpha) = \alpha$
<br>
Мы знаем, что $Z$ является распределением $N(0; 1)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta(\Delta) = \frac{1}{2} + \Phi_0(z_\alpha - \frac{\sqrt{nm}}{\sqrt{m\sigma^2_X + n\sigma^2_Y}}\cdot \Delta)$, где $\Delta = \mu_X - \mu_Y$. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(T(\vec{X}) > T(\vec{x})) = P_{H_0}(Z > z_{стат}) = 1 - P_{H_0}(Z < z_{стат}) = 1 - F_Z(z_{стат}) = \frac{1}{2} - \Phi_0(z_{стат})}$

<hr>'''),
            18:
                (r'''По двум независимым выборкам $X_1, X_2, . . . , X_n$ объема n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2, . . . , Y_m$ объема m из $N(\mu_Y; \sigma^2_Y)$, когда $\sigma^2_X = Var(X)$ и $\sigma^2_Y = Var(Y)$ – известны, проверяется на уровне значимости $\alpha$
основная гипотеза $H_0$ : $\mu_X = \mu_Y$ против альтернативной гипотезы $H_1$ : $\mu_X \neq \mu_Y$ . 1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$. 2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$, причём $Var(X)\ и\ Var(Y)$ - известны.
- Основная гипотеза $H_0: \mu_X=\mu_Y$
- Альтернативная гипотеза $H_0: \mu_X \neq \mu_Y$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{Z = \frac{\overline X - \overline Y}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{z_\alpha; +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ Z \sim N(0; 1)}$
<br>
При выполнении нулевой гипотезы, $\mu_X = \mu_Y$. Исходя из центральной предельной теоремы, величина $Z$ распределена по нормальному закону.
<br>
$E(Z) = E\left(\frac{\overline X - \overline Y}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}\right) = \frac{E(\overline X) - E(\overline Y)}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}} = \frac{E(X) - E(Y)}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}} \stackrel{\color{lightgreen}{\mu_X = \mu_Y}}{=} 0$.
<br>
$Var(Z) = Var\left(\frac{\overline X - \overline Y}{\sqrt{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}\right) = \frac{Var(\overline X) + Var(\overline Y)}{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}} = \frac{{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}}{{\frac{\sigma^2_X}{n} + \frac{\sigma^2_Y}{m}}} = 1$
<br>
Получили, что $Z \sim N(0; 1)$


2. $\color{orange}{Критерий,\ основанный\ на\ Z\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(|Z| > z_\frac{\alpha}{2}) = P_{H_0}(Z < -z_\frac{\alpha}{2}) + P_{H_0}(Z > z_\frac{\alpha}{2}) = 1 - P_{H_0}(Z > z_{1 - \frac{\alpha}{2}}) + \frac{\alpha}{2} = 1 - 1 + \frac{\alpha}{2} + \frac{\alpha}{2} = \alpha$
<br>
Мы знаем, что $Z$ является распределением $N(0; 1)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\frac \alpha 2$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta(\Delta) = \Phi_0(z_\alpha - \frac{\sqrt{nm}}{\sqrt{m\sigma^2_X + n\sigma^2_Y}}\cdot \Delta) + \Phi_0(z_\alpha + \frac{\sqrt{nm}}{\sqrt{m\sigma^2_X + n\sigma^2_Y}}\cdot \Delta)$, где $\Delta = \mu_X - \mu_Y$. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1, p_2\} = P_{H_0}(|Z(\vec{X})| > |Z(\vec{x})|) = P_{H_0}(|Z| > |z_{стат}|) = P_{H_0}(Z < -|z_{стат}|) + P_{H_0}(Z > |z_{стат}|) = F_Z(-|z_{стат}|) + 1 - F_Z(|z_{стат}|) = \frac{1}{2} - \Phi_0(|z_{стат}|) + 1 - \frac{1}{2} - \Phi_0(|z_{стат}|) = 1 - 2\Phi_0(|z_{стат}|)}$

<hr>'''),
            19:
                (r'''По двум независимым выборкам $X_1, X_2, . . . , X_n$ объема n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2, . . . , Y_m$ объема m из $N(\mu_Y; \sigma^2_Y)$, с независимыми но равными дисперсиями $\sigma^2_X = \sigma^2_Y = \sigma$ проверяется на уровне значимости $\alpha$
основная гипотеза $H_0$ : $\mu_X = \mu_Y$ против альтернативной гипотезы $H_1$ : $\mu_X > \mu_Y$ . 1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$. 2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$, причём $Var(X) = Var(Y) = \sigma^2$, но неизвестны.
- Основная гипотеза $H_0: \mu_X=\mu_Y$
- Альтернативная гипотеза $H_0: \mu_X > \mu_Y$

В качестве несмещённой оценки параметра $\sigma^2$ используется объединённая исправленная выборочная дисперсия:

$s_p^2 = \frac{n - 1}{n + m - 2}s_X^2 + \frac{m-1}{n+m-2}s_Y^2 = \frac{\sum_{k = 1}^n(X_k-\overline X)^2 + \sum_{k = 1}^m(Y_k-\overline Y)^2}{n+m-2}$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{T = \frac{\overline X - \overline Y}{s_p\sqrt{\frac{1}{n} + \frac{1}{m}}}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{t_\alpha(n+m-2); +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ T \sim t(n+m-2)}$
<br>
При выполнении нулевой гипотезы, $\mu_X = \mu_Y$.
<br>
$\Large T = \frac{\overline X - \overline Y}{s_p\sqrt{\frac{1}{n} + \frac{1}{m}}} \stackrel{\color{lightgreen}{\cdot\frac1\sigma}}{=} \frac{\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}}{\frac1\sigma\sqrt{\frac{\sum_{k = 1}^n(X_k-\overline X)^2 + \sum_{k = 1}^m(Y_k-\overline Y)^2}{n+m-2}}} =
\frac{Z}{\sqrt{\frac{\sum_{k = 1}^n\left(\frac{X_k-\overline X}{\sigma}\right)^2 + \sum_{k = 1}^m\left(\frac{Y_k-\overline Y}{\sigma}\right)^2}{n+m-2}}} =
\frac{Z}{\sqrt{\frac{\chi^2_{n-1} + \chi^2_{m-1}}{n+m-2}}} =
\frac{Z}{\sqrt{\frac{\chi^2_{n+m-2}}{n+m-2}}} \stackrel{\color{lightgreen}{опр.}}{=} t(n+m-2)$.
<br>
Пояснение: величина $\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right)$, согласно центральной предельной теореме, принадлежит нормальному закону (так как состоит из них), а математическое ожидание и дисперсия равны 0 и 1 соотвественно (см. ниже), поэтому $\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right) = Z \sim N(0; 1)$
<br>
$E\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right) = \frac{E(\overline X) + E(\overline Y)}{\sigma \sqrt{\frac1n + \frac1m}} \stackrel{\color{lightgreen}{\mu_X = \mu_Y}}{=} 0$
<br>
$Var\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right) = \frac{Var(\overline X) + Var(\overline Y)}{\sigma^2 \cdot (\frac1n + \frac1m)} = \frac{\frac{\sigma^2}{n} + \frac{\sigma^2}{m}}{\sigma^2 \cdot (\frac1n + \frac1m)} = 1$


2. $\color{orange}{Критерий,\ основанный\ на\ T\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(T > t_\alpha) = \alpha$
<br>
Мы знаем, что $T$ является распределением Стьюдента $t(n + m - 2)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(T(\vec{X}) > T(\vec{x})) = P_{H_0}(T > t_{стат}) = 1 - P_{H_0}(T < t_{стат}) = 1 - t_{n+m-2}(t_{стат})}$

<hr>'''),
            20:
                (r'''По двум независимым выборкам $X_1, X_2, . . . , X_n$ объема n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2, . . . , Y_m$ объема m из $N(\mu_Y; \sigma^2_Y)$, с независимыми но равными дисперсиями ;$\sigma^2_X = \sigma^2_Y = \sigma$; проверяется на уровне значимости $\alpha$
основная гипотеза $H_0$ : $\mu_X = \mu_Y$ против альтернативной гипотезы $H_1$ : $\mu_X \neq \mu_Y$ . 1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$. 2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$, причём $Var(X) = Var(Y) = \sigma^2$, но неизвестны.
- Основная гипотеза $H_0: \mu_X=\mu_Y$
- Альтернативная гипотеза $H_0: \mu_X \neq \mu_Y$

В качестве несмещённой оценки параметра $\sigma^2$ используется объединённая исправленная выборочная дисперсия:

$s_p^2 = \frac{n - 1}{n + m - 2}s_X^2 + \frac{m-1}{n+m-2}s_Y^2 = \frac{\sum_{k = 1}^n(X_k-\overline X)^2 + \sum_{k = 1}^m(Y_k-\overline Y)^2}{n+m-2}$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{T = \frac{\overline X - \overline Y}{s_p\sqrt{\frac{1}{n} + \frac{1}{m}}}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\left(-
\infty; -t_\frac\alpha2(n+m-2)\right) \cup \left(t_\frac\alpha2(n+m-2); +\infty\right)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ T \sim t(n+m-2)}$
<br>
При выполнении нулевой гипотезы, $\mu_X = \mu_Y$.
<br>
$\Large T = \frac{\overline X - \overline Y}{s_p\sqrt{\frac{1}{n} + \frac{1}{m}}} \stackrel{\color{lightgreen}{\cdot\frac1\sigma}}{=} \frac{\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}}{\frac1\sigma\sqrt{\frac{\sum_{k = 1}^n(X_k-\overline X)^2 + \sum_{k = 1}^m(Y_k-\overline Y)^2}{n+m-2}}} =
\frac{Z}{\sqrt{\frac{\sum_{k = 1}^n\left(\frac{X_k-\overline X}{\sigma}\right)^2 + \sum_{k = 1}^m\left(\frac{Y_k-\overline Y}{\sigma}\right)^2}{n+m-2}}} =
\frac{Z}{\sqrt{\frac{\chi^2_{n-1} + \chi^2_{m-1}}{n+m-2}}} =
\frac{Z}{\sqrt{\frac{\chi^2_{n+m-2}}{n+m-2}}} \stackrel{\color{lightgreen}{опр.}}{=} t(n+m-2)$.
<br>
Пояснение: величина $\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right)$, согласно центральной предельной теореме, принадлежит нормальному закону (так как состоит из них), а математическое ожидание и дисперсия равны 0 и 1 соотвественно (см. ниже), поэтому $\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right) = Z \sim N(0; 1)$
<br>
$E\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right) = \frac{E(\overline X) + E(\overline Y)}{\sigma^2 \cdot (\frac1n + \frac1m)} \stackrel{\color{lightgreen}{\mu_X = \mu_Y}}{=} 0$
<br>
$Var\left(\frac{\overline X - \overline Y}{\sigma \sqrt{\frac1n + \frac1m}}\right) = \frac{Var(\overline X) + Var(\overline Y)}{\sigma^2 \cdot (\frac1n + \frac1m)} = \frac{\frac{\sigma^2}{n} + \frac{\sigma^2}{m}}{\sigma^2 \cdot (\frac1n + \frac1m)} = 1$


2. $\color{orange}{Критерий,\ основанный\ на\ T\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(T > t(n+m-2)_{\frac{\alpha}{2}}) + P_{H_0}(T < -t(n+m-2)_{\frac{\alpha}{2}}) = \frac{\alpha}{2} + 1 - P_{H_0}(T > t(n+m-2)_{1 - \frac{\alpha}{2}}) = \alpha$
<br>
Мы знаем, что $T$ является распределением Стьюдента $t(n + m - 2)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\frac\alpha2$ по определению.


3. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1, p_2\} = P_{H_0}(|T(\vec{X})| > |T(\vec{x})|) = P_{H_0}(T < -|t_{стат}|) + P_{H_0}(T > |t_{стат}|) = 1 - P_{H_0}(T < |t_{стат}|) + 1 - P_{H_0}(T < |t_{стат}|) = 2 - 2t_{n+m-2}(|t_{стат}|)}$

<hr>'''),
            21:
                (r'''По двум независимым выборкам $X_1, X_2, . . . , X_n$ объема n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2, . . . , Y_m$ объема m из $N(\mu_Y; \sigma^2_Y)$ c неизвестными и не равными дисперсиями, проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \mu_X = \mu_Y$ против альтернативной гипотезы $H_1 : \mu_X \neq \mu_Y$ (проблема Беренса-Фишера). 1) Приведите статистику критерия Уэлча и критическое множество для проверки $H_0$ против $H_1$. 2) Приведите основное свойство статистики критерия. 3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$, причём $Var(X) \neq Var(Y)$ - неизвестны.
- Основная гипотеза $H_0: \mu_X=\mu_Y$
- Альтернативная гипотеза $H_0: \mu_X \neq \mu_Y$

В качестве несмещённой оценки параметра $\sigma^2$ используется следующая статистика:

$s_w^2 = \frac{s_X^2}{n} + \frac{s_Y^2}{m}$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ Уэлч предложил использовать следующую статистику:
$\large \color{orange}{T_w = \frac{\overline X - \overline Y}{s_w}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{\left(-
\infty; -s_w\cdot t_\frac\alpha2(\widehat{df})\right) \cup \left(s_w\cdot t_\frac\alpha2(\widehat{df}); +\infty\right)\}}$

Приведём основное свойство критерия:

$\color{orange}{Если\ H_0\ верна,\ то\ T \approx t(\widehat{df})}$, где
<br>
$\large \widehat{df} = \frac{\left(\frac{s_X^2}{n} + \frac{s_Y^2}{m}\right)}{\frac{s_X^4}{n^2(n-1)} + \frac{s_Y^4}{m^2(m-1)}}$

<br>

$\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1, p_2\} = P_{H_0}(|T(\vec{X})| > |T(\vec{x})|) = P_{H_0}(T < -|t_{стат}|) + P_{H_0}(T > |t_{стат}|) = 1 - P_{H_0}(T < |t_{стат}|) + 1 - P_{H_0}(T < |t_{стат}|) = 2 - 2t_{\widehat{df}}(|t_{стат}|)}$

<hr>'''),
            22:
                (r'''По двум независимым выборкам $X_1,X_2,...X_n$ объема $n$ из $N(\mu_X; \sigma^2_X)$ и $Y_1,Y_2,...Y_m$ объема $m$ из $N(\mu_Y; \sigma^2_Y)$ проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma_X^2 = \sigma_Y^2$ против альтернативной гипотезы $H_1 : \sigma_X^2 > \sigma_Y^2$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$.
- Основная гипотеза $H_0: \sigma^2_X=\sigma^2_Y$
- Альтернативная гипотеза $H_0: \sigma^2_X > \sigma^2_Y$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{\mathbb F = \frac{s_X^2}{s_Y^2}}$, где $s^2$ - исправленные выборочные дисперсии.

Критическая область:
$\color{orange}{K_{\alpha} = \{f_\alpha(n - 1; m - 1); +\infty\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \mathbb F \sim F(n - 1; m - 1)}$
<br>
При выполнении нулевой гипотезы, $\sigma^2_X = \sigma^2_Y = \sigma^2$.
<br>
$\large \mathbb F = \frac{s^2_X}{s^2_Y} \stackrel{\color{lightgreen}{\cdot \frac{1}{\sigma^2}}}{=} \frac{\frac{(n - 1)s_X^2}{\sigma^2}\cdot\frac{1}{n - 1}}{\frac{(m - 1)s_Y^2}{\sigma^2}\cdot\frac{1}{m - 1}} = \frac{\frac{\chi^2_X(n-1)}{n - 1}}{\frac{\chi^2_Y(m-1)}{m - 1}} \stackrel{\color{lightgreen}{опр.}}{=} F(n - 1; m - 1)$


2. $\color{orange}{Критерий,\ основанный\ на\ \mathbb F\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\mathbb F > f_\alpha(n - 1; m - 1)) = \alpha$
<br>
Мы знаем, что $\mathbb F$ является распределением Фишера $F(n - 1; m - 1)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\alpha$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta(\lambda) = F_{n-1; m-1}(\lambda \cdot f_\alpha(n-1; m-1))$, где $\lambda = \frac{\sigma^2_Y}{\sigma^2_X}$. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = P_{H_0}(F(\vec{X}) > F(\vec{x})) = P_{H_0}(F > f_{стат}) = 1 - P_{H_0}(F < f_{стат}) = 1 - f_{n-1; m-1}(f_{стат})}$

<hr>'''),
            23:
                (r'''По двум независимым выборкам $X_1,X_2,...X_n$ объема $n$ из $N(\mu_X; \sigma^2_X)$ и $Y_1,Y_2,...Y_m$ объема $m$ из $N(\mu_Y; \sigma^2_Y)$ проверяется на уровне значимости $\alpha$ основная гипотеза $H_0 : \sigma_X^2 = \sigma_Y^2$ против альтернативной гипотезы $H_1 : \sigma_X^2 \neq \sigma_Y^2$.

1) Приведите необходимую статистику критерия и критическое множество для проверки $H_0$ против $H_1$.
2) Приведите (с доказательством) основные свойства критерия.
3) Приведите (с выводом) выражение для P-значения критерия.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$.
- Основная гипотеза $H_0: \sigma^2_X=\sigma^2_Y$
- Альтернативная гипотеза $H_0: \sigma^2_X \neq \sigma^2_Y$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{\mathbb F = \frac{s_X^2}{s_Y^2}}$, где $s^2$ - исправленные выборочные дисперсии.

Критическая область:
$\color{orange}{K_{\alpha} = \{\left(0; f_{1-\frac\alpha2}(n-1; m-1)\right) \cup \left(f_\frac\alpha2(n - 1; m - 1); +\infty\right)\}}$

Свойства:
1. $\color{orange}{Если\ H_0\ верна,\ то\ \mathbb F \sim F(n - 1; m - 1)}$
<br>
При выполнении нулевой гипотезы, $\sigma^2_X = \sigma^2_Y = \sigma^2$.
<br>
$\large \mathbb F = \frac{s^2_X}{s^2_Y} \stackrel{\color{lightgreen}{\cdot \frac{1}{\sigma^2}}}{=} \frac{\frac{(n - 1)s_X^2}{\sigma^2}\cdot\frac{1}{n - 1}}{\frac{(m - 1)s_Y^2}{\sigma^2}\cdot\frac{1}{m - 1}} = \frac{\frac{\chi^2_X(n-1)}{n - 1}}{\frac{\chi^2_Y(m-1)}{m - 1}} \stackrel{\color{lightgreen}{опр.}}{=} F(n - 1; m - 1)$


2. $\color{orange}{Критерий,\ основанный\ на\ \mathbb F\ статистике,\ имеет\ уровень\
значимости\ \alpha}$ (т.е. вероятность совершить ошибку первого рода
(отклонить верную гипотезу $H_0$) в точности равна $\alpha$).
<br>
Вероятность совершить ошибку первого рода можно записать с помощью критической области, а также, зная это область, можно переписать в виде вероятности.
$ \alpha = P_{H_0}((X_1, X_1, . . . , X_n) \in K) = P_{H_0}(\mathbb F > f_{\frac{\alpha}{2}}(n-1; m-1)) + P_{H_0}(\mathbb F < f_{1 - \frac{\alpha}{2}}(n-1; m-1)) = \frac{\alpha}{2} + 1 - P_{H_0}(\mathbb F > f_{1 - \frac{\alpha}{2}}(n-1; m-1)) = \alpha$
<br>
Мы знаем, что $\mathbb F$ является распределением Фишера $F(n - 1; m - 1)$ при выполнении $H_0$, а следовательно данная вероятность это верхняя процентная точка этого распределения в точке $\frac\alpha2$ по определению.


3. $\color{orange}{Вероятность\ ошибки\ 2\ рода\ и\ мощность\ критерия}$
<br>
Вероятность ошибки 2 рода, это вероятность принять $H_0$ гипотезу, когда она была неверна. Это значение равно $\beta(\lambda) = F_{n-1; m-1}(\lambda \cdot f_\frac\alpha2(n-1; m-1)) - F_{n-1; m-1}(\lambda \cdot f_{1 - \frac\alpha2}(n-1; m-1))$, где $\lambda = \frac{\sigma^2_Y}{\sigma^2_X}$. Мощность критерия в этом случае задаётся как $W = 1 - \beta$


4. $\color{orange}{Выражение\ для\ pv\ значения}$
<br>
Формула p-value:
$\color{orange}{PV = 2min\{p_1; p_2\} =
2min\{P_{H_0}(\mathbb F < f_{стат}); P_{H_0}(\mathbb F > f_{стат})\} = 2min\{F_{n-1; m-1}(f_{стат}); 1 - F_{n-1; m-1}(f_{стат})\}}$

<hr>'''),
            24:
                (r'''По двум независимым выборкам $X_1, X_2, . . . , X_n$ объема n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2, . . . , Y_m$ объема m из $N(\mu_Y; \sigma^2_Y)$, с независимыми но равными дисперсиями $\sigma^2_X = \sigma^2_Y = \sigma$ проверяется на уровне значимости $\alpha$
основная гипотеза $H_0$ : $\mu_X = \mu_Y$ против альтернативной гипотезы $H_1$ : $\mu_X \neq \mu_Y$ .
1) Приведите необходимую статистику F – критерия однофакторного дисперсионного анализа и критическое множество для проверки $H_0$ против $H_1$. 2) Приведите (с выводом и необходимыми пояснениями в обозначениях) обоснование равенства процентных точек $f_{\alpha}(1; n + m - 2)$распределения Фишера и $t^2_{\frac {\alpha}{2}}(n + m - 2)$ распределения Стьюдента с n + m - 2 свободы.''',
                 r'''Пусть $X_1, X_2,...,X_n$ - выборка объёма n из $N(\mu_X; \sigma^2_X)$ и $Y_1, Y_2,...,Y_n$ - выборка объёма m из $N(\mu_Y; \sigma^2_Y)$, причём $Var(X) = Var(Y)$, но неизвестны.
- Основная гипотеза $H_0: \mu_X=\mu_Y$
- Альтернативная гипотеза $H_0: \mu_X \neq \mu_Y$

Для проверки основной гипотезы $H_0$ против альтернативной гипотезы $H_1$ используется следующая статистика:
$\large \color{orange}{\mathbb F = \frac{MSTR}{MSE} = \frac{\frac{SSTR}{k-1}}{\frac{SSE}{n - k}} = \frac{\frac{n\delta^2}{k-1}}{\frac{n\overline{\sigma^2}}{n - k}}}$

Критическая область:
$\color{orange}{K_{\alpha} = \{f_\alpha(k-1; n-k); +\infty\}}$

**2) Обоснование равенства**

Хи-квадрат: $\chi^2_n = \sum_{i=1}^{n}{Z^2_i}$$\chi^2_n = \sum_{i=1}^{n}{Z^2_i}$, где $Z \sim N(0, 1)$$Z \sim N(0, 1)$

Распределение Фишера: $\Large \mathbb F(n, m) = \frac{\frac{\chi^2_n}{n}}{\frac{\chi^2_m}{m}}$$\Large \mathbb F(n, m) = \frac{\frac{\chi^2_n}{n}}{\frac{\chi^2_m}{m}}$

Распределение Стьюдента: $\Large T(n) = \frac{Z}{\sqrt{\frac{\chi^2_n}{n}}}$$\Large T(n) = \frac{Z}{\sqrt{\frac{\chi^2_n}{n}}}$

Определение верхней процентной точки: $P(X > x_\alpha) = \alpha$

Свойство верхней процентной точки распр. Стьюдента: $t_{1 - \alpha}(k) = -t_\alpha(k)$$t_{1 - \alpha}(k) = -t_\alpha(k)$


***Решение***

Возведём распр. Стьюдента в квадрат:

$\Large T^2(m) = \frac{Z^2}{\frac{\chi^2_m}{m}} = \frac{\frac{\chi^2_1}{1}}{\frac{\chi^2_m}{m}} = \mathbb F(1, m)$

Рассмотрим верхнюю процентную точку распределения Фишера по определению:

$P(F > f_\alpha) = \alpha$

По доказанному:

$P(T^2 > f_\alpha) = \alpha$

Из условия:

$P(T^2 > t^2_{\frac{\alpha}{2}}) = \alpha$

$P(|T| > |t_{\frac{\alpha}{2}}|) = \alpha$

$P(T < -t_{\frac{\alpha}{2}}) + P(T > t_{\frac{\alpha}{2}}) = \alpha$

Используя свойство верхней процентной точки:

$P(T < t_{1 - \frac{\alpha}{2}}) + P(T > t_{\frac{\alpha}{2}}) = \alpha$

$1 - P(T > t_{1 - \frac{\alpha}{2}}) + P(T > t_{\frac{\alpha}{2}}) = \alpha$

Обратно по определению верхней процентной точки:

$1 - 1 + \frac{\alpha}{2} + \frac{\alpha}{2} = \alpha$ - тождество, а значит $f_α(1; m) = t^2_{\frac{α}{2}}(m)$ верно

<hr>'''),
        },
        "Q3": {
            1:
                (r'''Пусть $X_1, X_2, . . . , X_6$ – выборка из равномерного распределения на отрезке [5;8], $\hat F(x)$ – соответствующая выборочная функция распределения. Найдите: а) вероятность $P (\hat F(6) = \hat F(8)$ ; б) вероятность $P(\hat F(7) = \frac {1}{2})$''',
                 r'''$P(\widehat F_n(x) = \frac{k}{n}) = C_n^k p^k q^{n-k}$
```
X = uniform(5, 3)
n = 6

# a)
# так как f(6) = f(8), то для этого не нужно, чтобы были числа между 6 и 8,
# иными словами - все числа были до 6, то есть f(6) = 1
k = 1 * n
resa = math.comb(n, k) * X.cdf(6) ** k * X.sf(6) ** (n - k)

# b)
k = int((1 / 2) * n)
resb = math.comb(n, k) * X.cdf(7) ** k * X.sf(7) ** (n - k)

resa, resb
```'''),
            2:
                (r'''Имеется выборка $X_1, X_2, . . . , X_n$ объема n из генеральной совокупности с функцией распределения F(x). Найдите функции распределения экстремальных статистик $X_{(1)}$ и $X_{(n)}$.''',
                 r'''$F_{X_{(n)}}(x) \stackrel{\color{\lightgreen}{опр.}}{=} P(X_{(n)} \leq x) = P(X_1 \leq x,\ ...,\ X_n \leq x) \stackrel{\color{\lightgreen}{независ.}}{=} P(X_1 \leq x)\cdot\ ...\ \cdot P(X_n \leq x) \stackrel{\color{\lightgreen}{опр.}}{=} F(x) \cdot\ ...\ \cdot F(x) = F^n(x)$

<br>

$F_{X_{(1)}}(x) \stackrel{\color{\lightgreen}{опр.}}{=} P(X_{(1)} \leq x) = 1 - P(X_{(1)} > x) = 1 - P(X_1 > x,\ ...,\ X_n > x) \stackrel{\color{\lightgreen}{независ.}}{=} 1 - P(X_1 > x)\cdot\ ...\ \cdot P(X_n > x) = 1 - (1 - P(X_1 \leq x))\cdot\ ...\ \cdot (1 - P(X_n \leq x)) \stackrel{\color{\lightgreen}{опр.}}{=} 1 - (1 - F(x)) \cdot\ ...\ \cdot (1 - F(x)) = 1 - (1 - F(x))^n$

<hr>'''),
            3:
                (r'''Пусть X и Y – две независимые несмещенные оценки параметра θ с дисперсиями $\sigma^2$ и $4\sigma^2$ соответственно. a) Является ли $X^2$ несмещенной оценкой параметра $\theta^2$? б) Является ли Z = X $\cdot$ Y несмещенной оценкой параметра $\theta^2$?''',
                 r'''а)
$Var(X) = E(X^2) - E^2(X)$

$E(X^2) = Var(X) + E^2(X) = \sigma^2 + \theta^2 \neq \theta^2 \Rightarrow$ оценка смещённая

<br>

б)
$E(X\cdot Y) \stackrel{\color{\lightgreen}{независ.}}{=} E(X)\cdot E(Y) = \theta \cdot \theta = \theta^2 \Rightarrow$ оценка несмещённая

<hr>'''),
            4:
                (r'''Пусть $\hat \theta = T(X_1, . . . , X_n)$ оценка параметра $\theta, а b = (E[\hat\theta] - \theta)$ – смещение. Доказать формулу $\Delta =
Var(\hat \theta) + b^2$, где $\Delta = E[(\hat\theta - \theta)^2]$ – среднеквадратичная ошибка оценки.''',
                 r'''Необходимые факты:

$Var(X) = E(X^2) - E^2(X)$, откуда

$E(X^2) = Var(X) + E^2(X)$

<br>

$Var(X + const) = Var(X)$

<br>

Здесь $\theta$ без крышки - это константное значение

<br>

Решение:

$\Delta = E((\hat\theta - \theta)^2) = Var(\hat\theta - \theta) + E^2(\hat\theta - \theta) = Var(\hat\theta) + (E(\hat\theta) - \theta)^2 = Var(\hat\theta) + b^2$

<hr>'''),
            5:
                (r'''Пусть $X_1, X_2$ – выборка объема 2 из некоторого распределения с генеральным средним $\theta$ = E(X) и дисперсией $\sigma^2 = Var(X)$. В качестве оценки параметра $\theta$ используется оценка вида $\hat \theta = aX_1+2aX_2$.Известно отношение $\frac{\sigma^2}{\sigma^2}=\frac {3}{5}$. Найдите оценку с наименьшей среднеквадратической ошибкой. Является ли эта оценка несмещенной?''',
                 r'''По условию, $\sigma^2 = \frac{3}{5}\theta^2$

(равенство из задания выше)

$\Delta = Var(\hat\theta) + (E(\hat\theta - \theta))^2 = \alpha^2 Var(X) + 4\alpha^2 Var(X) + (\alpha E(X) + 2\alpha E(X) - \theta)^2 = \alpha^2 \sigma^2 + 4\alpha^2\sigma^2 + (3\alpha\theta - \theta)^2 = 5\alpha^2 \cdot \frac{3}{5}\theta^2 + 9\alpha^2\theta^2 - 6\alpha\theta^2 + \theta^2 = \theta^2(12\alpha^2 - 6\alpha + 1)$

<br>

Т.к. $\theta^2 > 0$, то для нахождения наименьшей оценки необходимо минимизировать $(12\alpha^2 - 6\alpha + 1)$. Это парабола с ветвями вверх, а значит минимум в вершине $-\frac{b}{2a}$:

$\alpha^* = \frac{6}{2\cdot12} = \frac{1}{4}$

<br>

Получили следующую оценку:

$\hat\theta = \frac{1}{4}X_1 + \frac{1}{2}X_2$

<br>

$E(\hat\theta) = \frac{1}{4}E(X_1) + \frac{1}{2}E(X_2) = \frac{3}{4}\theta \neq \theta \Rightarrow$ оценка смещённая

<hr>'''),
            6: (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка объема n из распределения $\mathcal{L}$ с моментами $\nu_1 = \nu_1(X) = E(X)$, $\mu_2 = \mu_2(X) = \sigma^2 = Var(X)$, $\mu_k = \mu_k(X) = E[(X − E(X))^k]$, k = 3, 4. Покажите, что

a) $\mu_3(\overline X) = \frac {\mu_3(X)}{n^2}$;
b) $\mu_4(\overline X) = \frac {\mu_4(X)}{n^3}
+
\frac {3(n − 1)}{n^3}\mu^2_2(X)$;''',
                r'''а)
$\mu_3(\overline X) \stackrel{\color{\lightgreen}{опр. \overline X}}{=}
\mu_3(\frac{X_1 + X_2 + ... + X_n}{n}) \stackrel{\color{\lightgreen}{опр.\mu_3}}{=}
E\left[\left((\frac{X_1 + X_2 + ... + X_n}{n} - E(\frac{X_1 + X_2 + ... + X_n}{n})\right)^3\right] =
E\left[\left(\frac{1}{n}(X_1 + X_2 + ... + X_n) - \frac{1}{n}E(X_1 + X_2 + ... + X_n)\right)^3\right] =
\frac{1}{n^3}E\left[\left((X_1 - E(X_1) + ... + X_n - E(X_n)\right)^3\right] \stackrel{\color{lightgreen}{t_i = X_i - E(X_i)}}{=}
\frac{1}{n^3}E\left[(t_1 + t_2 + ... + t_n)^3\right] =
\frac{1}{n^3}E\left[t_1^3 + t_2^3 + ... 3t_1^2t_2 + ...\right] \stackrel{\color{\lightgreen}{независ.}}{=}
\frac{1}{n^3}\left(\sum_{i=1}^n{E(t_i^3)} + \sum_{i=1, j=1}^n{3E(t_i^2)E(t_j))}\right) \stackrel{\color{lightgreen}{E(t_i) = E(X_i - E(X_i)) = 0}}{=}
\frac{1}{n^3}\left(\sum_{i=1}^n{E(t_i^3)}\right) =
\frac{1}{n^3}\left(\sum_{i=1}^n{E\left[(X_i - E(X_i))^3\right]}\right) \stackrel{\color{\lightgreen}{опр. \mu_3}}{=}
\frac{1}{n^3}\left(\sum_{i=1}^n{\mu_3}\right) =
\frac{n\mu_3}{n^3} =
\frac{\mu_3}{n^2}$

<br>

б)
$\mu_4(\overline X) \stackrel{\color{\lightgreen}{опр. \overline X}}{=}
\mu_4(\frac{X_1 + X_2 + ... + X_n}{n}) \stackrel{\color{\lightgreen}{опр.\mu_4}}{=}
E\left[\left((\frac{X_1 + X_2 + ... + X_n}{n} - E(\frac{X_1 + X_2 + ... + X_n}{n})\right)^4\right] =
E\left[\left(\frac{1}{n}(X_1 + X_2 + ... + X_n) - \frac{1}{n}E(X_1 + X_2 + ... + X_n)\right)^4\right] =
\frac{1}{n^4}E\left[\left((X_1 - E(X_1) + ... + X_n - E(X_n)\right)^4\right] \stackrel{\color{lightgreen}{t_i = X_i - E(X_i)}}{=}
\frac{1}{n^4}E\left[(t_1 + t_2 + ... + t_n)^4\right] =
\frac{1}{n^4}E\left[(t_1 + t_2 + ... + t_n)^4\right] =
\frac{1}{n^4}E\left[t_1^4 + t_2^4 + ... 4t_1^3t_2 + ... + 6t_1^2t_2^2 + ... + 12t_1^2t_2t_3 + ...\right] \stackrel{\color{\lightgreen}{независ.}}{=}
\frac{1}{n^4}\left(\sum_{i=1}^n{E(t_i^4)} + \sum_{i=1, j=1}^n{4E(t_i^3)E(t_j)} + \sum_{i=1, j=1}^n{6E(t_i^2)E(t_j^2)} + \sum_{i=1, j=1, k=1}^n{12E(t_i^2)E(t_j)E(t_k)}\right) \stackrel{\color{lightgreen}{E(t_i) = E(X_i - E(X_i)) = 0}}{=}
\frac{1}{n^4}\left(\sum_{i=1}^n{E(t_i^4)} + \sum_{i=1, j=1}^n{6E(t_i^2)E(t_j^2)}\right) \stackrel{\color{lightgreen}{опр. \mu_k}}{=}
\frac{1}{n^4}\left(\sum_{i=1}^n{\mu_4} + \sum_{i=1, j=1}^n{6\mu_2\mu_2}\right) \stackrel{\color{lightgreen}{C_n^2 = \frac{n(n-1)}{2}}}{=}
\frac{1}{n^4}\left(n{\mu_4} + 3n(n-1)\mu_2^2\right) =
\frac{\mu_4}{n^3} + \frac{3(n-1)}{n^3}\mu_2^2$

<hr>'''),
            7: (r'''Пусть $X_1, X_2, X_3$ – выборка из генерального распределения с математическим ожиданием $\mu$ и дисперсией $\theta = \sigma^2$. Рассмотрим две оценки параметра $\theta$: a) $\hat \theta_1 = c_1(X_1 - X_2)^2$; б) $\hat \theta_2 = c_2[(X_1 − X_2)^2 + (X_1−X_3)^2+(X_2−X_3)^2]$. Найдите значения $c_1$ и $c_2$ такие, что оценки $\hat \theta_1$ и $\hat \theta_2$ являются несмещенными оценками параметра дисперсии $\sigma^2$.''',
                r'''Условие несмещённости:

$E(\hat\theta_1) = \sigma^2$

<br>

а)
$E(\hat\theta_1) = c_1E(X_1 - X_2)^2 = c_1(Var(X_1 - X_2) + E^2(X_1 - X_2)) =
c_1(Var(X_1) + Var(X_2) + (E(X_1) - E(X_2))^2) = c_1(\sigma^2 + \sigma^2 + 0^2)= c_1\cdot 2\sigma^2$

Приравнивая к $\sigma^2$, получаем:

$2c_1\sigma^2 = \sigma^2$

$c_1 = \frac{1}{2}$ - при таком $c_1$ оценка несмещённая

<br>

б)
$E(\hat\theta_2) = c_2\left[E\left((X_1 - X_2)^2\right) + E\left((X_1 - X_3)^2\right) + E\left((X_1 - X_2)^2\right)\right] =
c_2\left[Var(X_1) + Var(X_2) + E^2(X_1 - X_2) + Var(X_1) + Var(X_3) + E^2(X_1 - X_3) + Var(X_2) + Var(X_3) + E^2(X_2 - X_3)\right] =
c_2\left[\sigma^2 + \sigma^2 + 0 + \sigma^2 + \sigma^2 + 0 + \sigma^2 + \sigma^2 + 0\right] =
c_2\cdot 6\sigma^2$

Приравнивая к $\sigma^2$, получаем:

$6c_2\sigma^2 = \sigma^2$

$c_2 = \frac{1}{6}$ - при таком $c_2$ оценка несмещённая

<hr>'''),
            8:
                (r'''Пусть $X_1, X_2, X_3, X_4$ – выборка из $N(\theta; \sigma^2)$. Рассмотрим две оценки параметра \theta: $\hat \theta_1 = \frac {X_1+2X_2+3X_3+4X_4}{10} , \hat \theta_2 = \frac {X_1+4X_2+4X_3+X_4}{10}$ . a) Покажите, что обе оценки являются несмещенными для параметра θ; б) Какая из этих оценок является оптимальной?''',
                 r'''а)
$E(\hat\theta_1) = E(\frac{X_1 + 2X_2 + 3X_3 + 4X_4}{10}) =
\frac{E(X_1) + 2E(X_2) + 3E(X_3) + 4E(X_4)}{10} =
\frac{\theta + 2\theta + 3\theta + 4\theta}{10} = \theta \Rightarrow$ оценка несмещённая

$E(\hat\theta_2) = E(\frac{X_1 + 4X_2 + 4X_3 + X_4}{10}) =
\frac{E(X_1) + 4E(X_2) + 4E(X_3) + E(X_4)}{10} =
\frac{\theta + 4\theta + 4\theta + \theta}{10} = \theta \Rightarrow$ оценка несмещённая

<br>

б)
$Var(\hat\theta_1) = Var(\frac{X_1 + 2X_2 + 3X_3 + 4X_4}{10}) =
\frac{Var(X_1) + 4Var(X_2) + 9Var(X_3) + 16Var(X_4)}{100} =
\frac{30\sigma^2}{100} = 0.3\sigma^2$

$Var(\hat\theta_2) = Var(\frac{X_1 + 4X_2 + 4X_3 + X_4}{10}) =
\frac{Var(X_1) + 16Var(X_2) + 16Var(X_3) + Var(X_4)}{100} =
\frac{34\sigma^2}{100} = 0.34\sigma^2$

Т.к. $\sigma^2>0$, то

$0.3\sigma^2 < 0.34\sigma^2 \Rightarrow$ оценка $\hat\theta_1$ оптимальнее

<hr>'''),
            9:
                (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка из генерального распределения и пусть $\theta = E(X), \sigma^2 = Var(X)$– математическое ожидание и дисперсия. Рассмотрим следующие оценки параметра $\theta$: $\hat \theta_1 = \frac {X_1+X_2}{2}, \hat \theta_2 = \frac {X_1+X_n}{4} + \frac {X_2+...+X_{n−1}}{2(n−2)} , \hat \theta_3 = \overline X$. а) Будут ли эти оценки несмещенными для параметра θ? б) Какая из них является состоятельной для параметра $\theta$?''',
                 r'''а)
$E(\hat\theta_1) = E(\frac{X_1 + X_2}{2}) = \frac{E(X_1) + E(X_2)}{2} = \frac{2\theta}{2} = \theta \Rightarrow$ оценка несмещённая

$E(\hat\theta_2) = E(\frac{X_1+X_n}{4} + \frac{X_2 + ... + X_{n−1}}{2(n−2)}) = \frac{E(X_1) + E(X_n)}{4} + \frac{E(X_2) + ... + E(X_{n-1})}{2(n-2)} = \frac{\theta}{2} + \frac{(n-2)\theta}{2(n-2)} =
\theta \Rightarrow$ оценка несмещённая

$E(\hat\theta_3) = E(\overline X) = \frac{E(X_1) + ... + E(X_n)}{n} = \frac{n\theta}{n} = \theta \Rightarrow$ оценка несмещённая

<br>

б)
$Var(\hat\theta_1) = \frac{Var(X_1) + Var(X_2)}{4} = \frac{\sigma^2}{2}$

$Var(\hat\theta_1) \underset{n \rightarrow +\infty}{\longrightarrow} \frac{\sigma^2}{2} \Rightarrow$ оценка несостоятельная

<br>

$Var(\hat\theta_2) = \frac{Var(X_1) + Var(X_n)}{16} + \frac{Var(X_2) + ... + Var(X_{n - 1})}{4(n-2)^2} =
\frac{\sigma^2}{8} + \frac{\sigma^2}{4(n-2)}$

$Var(\hat\theta_2) \underset{n \rightarrow +\infty}{\longrightarrow} \frac{\sigma^2}{8} \Rightarrow$ оценка несостоятельная

<br>

$Var(\overline X) = \frac{Var(X_1) + ... + Var(X_n)}{n^2} =
\frac{\sigma^2}{n}$

$Var(\hat\theta_3) \underset{n \rightarrow +\infty}{\longrightarrow} 0 \Rightarrow$ оценка состоятельная

<hr>'''),
            10:
                (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка из равномерного распределения U([0; $\theta$]) c неизвестным параметром $\theta$ > 0. Требуется оценить параметр $\theta$. В качестве оценка параметра $\theta$ рассматриваются: $ \hat \theta_1 = 2 \overline X, \hat \theta_2 = \frac {n+1}{n} X_{(n)}$. а) Будут ли оценки несмещенными?; б) состоятельными? в) найдите среди них оптимальную.''',
                 r'''а)
$E(\hat\theta_1) = 2E(\overline X) = 2E(X) = 2\cdot \frac{0+\theta}{2} = \theta \Rightarrow$ оценка несмещённая

<br>

$F_{X_{(n)}}(x) \stackrel{\color{\lightgreen}{опр.}}{=} P(X_{(n)} \leq x) = P(X_1 \leq x,\ ...,\ X_n \leq x) \stackrel{\color{\lightgreen}{независ.}}{=} P(X_1 \leq x)\cdot\ ...\ \cdot P(X_n \leq x) \stackrel{\color{\lightgreen}{опр.}}{=} F(x) \cdot\ ...\ \cdot F(x) = F^n(x)$

$f_n(x) = (F^n)' = ((\frac{x-0}{\theta-0})^n)' = n\frac{x^{n-1}}{\theta^n}$

<br>

$E(\hat\theta_2) = \frac{n+1}{n}E(X_{(n)}) = \frac{n+1}{n}\int_0^\theta{xf(x)dx} = \frac{n+1}{n}\int_0^\theta{xn\frac{x^{n-1}}{\theta^n}dx} = \frac{n+1}{\theta^n}\cdot (\frac{x^{n+1}}{n+1}|_0^\theta) = \theta \Rightarrow$ оценка несмещённая

<br>

б)
$Var(\hat\theta_1) = 4\frac{Var(X_1) + ... + Var(X_n)}{n^2} = \frac{4}{n}\frac{(\theta - 0)^2}{12} = \frac{\theta^2}{3n}$

$Var(\hat\theta_1) \underset{n \rightarrow +\infty}{\longrightarrow} 0 \Rightarrow$ оценка состоятельная

<br>

$Var(\hat\theta_2) = \frac{(n+1)^2}{n^2}Var(X_{(n)}) =
\frac{(n+1)^2}{n^2}\left(\int_0^\theta{x^2f(x)dx} - E^2(X_{(n)}) \right) =
\frac{(n+1)^2}{n^2}\left(\int_0^\theta{x^2n\frac{x^{n-1}}{\theta^n}dx} - \frac{n^2}{(n+1)^2}\theta^2\right) =
\frac{(n+1)^2}{n\theta^n}\cdot\frac{\theta^{n+2}}{n+2}-\theta^2 =
\theta^2\left(\frac{(n+1)^2}{n^2+2n}-1\right) =
\frac{\theta^2}{n(n+2)}$

$Var(\hat\theta_2) \underset{n \rightarrow +\infty}{\longrightarrow} 0 \Rightarrow$ оценка состоятельная

<br>

в) Сравним оценки:

$\frac{\theta^2}{3n} \vee \frac{\theta^2}{n(n+2)}$

$\frac{1}{3} \geq \frac{1}{n+2}$ при $\forall n > 0 \Rightarrow$ оценка $\hat\theta_2$ оптимальнее

<hr>'''),
            11:
                (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка из равномерного распределения U([0; $\theta$]) c неизвестным параметром $\theta$ > 0. Требуется оценить параметр $\theta$. В качестве оценка параметра $\theta$ рассматриваются: $\hat \theta_1 = 2 \overline X, \hat \theta_2 = (n+1)X_{(1)}$. а) Будут ли оценки несмещенными?; б) Состоятельными? в) Найти среди них оптимальную.''',
                 r'''а)
$E(\hat\theta_1) = 2E(\overline X) = 2E(X) = 2\cdot \frac{0+\theta}{2} = \theta \Rightarrow$ оценка несмещённая

<br>

$F_{X_{(1)}}(x) \stackrel{\color{\lightgreen}{опр.}}{=} P(X_{(1)} \leq x) = 1 - P(X_{(1)} > x) = P(X_1 > x,\ ...,\ X_n > x) \stackrel{\color{\lightgreen}{независ.}}{=} 1 - P(X_1 > x)\cdot\ ...\ \cdot P(X_n > x) = 1 - (1 - P(X_1 \leq x))\cdot\ ...\ \cdot (1 - P(X_n \leq x)) \stackrel{\color{\lightgreen}{опр.}}{=} 1 - (1 - F(x)) \cdot\ ...\ \cdot (1 - F(x)) = 1 - (1 - F(x))^n$

$f_n(x) = (1 - (1 - F(x))^n)' = \frac{n}{\theta}\left(1 - \frac{x}{\theta}\right)^{n-1}$

<br>

$E(\hat\theta_2) = (n+1)E(X_{(1)}) = (n+1)\int_0^\theta{xf(x)dx} = (n+1)\int_0^\theta{x\frac{n}{\theta}\left(1 - \frac{x}{\theta}\right)^{n-1}dx} \stackrel{\color{lightgreen}{t = 1 - \frac{x}{\theta}}}{=}
-(n+1)n\int_1^0{\theta(1-t)t^{n-1}dt} =
\theta (n+1) n \cdot (\frac{t^n}{n} - \frac{t^{n+1}}{n+1})|_0^1 =
\theta(n+1)n\cdot (\frac{1}{n}-\frac{1}{n+1}) =
\theta \Rightarrow$

оценка несмещённая

<br>

б)
$Var(\hat\theta_1) = 4\frac{Var(X_1) + ... + Var(X_n)}{n^2} = \frac{4}{n}\frac{(\theta - 0)^2}{12} = \frac{\theta^2}{3n}$

$Var(\hat\theta_1) \underset{n \rightarrow +\infty}{\longrightarrow} 0 \Rightarrow$ оценка состоятельная

<br>

$Var(\hat\theta_2) = (n+1)^2Var(X_{(1)}) =
(n+1)^2\left(\int_0^\theta{x^2f(x)dx} - E^2(X_{(1)}) \right) =
(n+1)^2\left(\int_0^\theta{x^2\frac{n}{\theta}(1 - \frac{x}{\theta})^{n-1}dx} - \frac{\theta^2}{(n+1)^2}\right) \stackrel{\color{lightgreen}{t = 1 - \frac{x}{\theta}}}{=}
(n+1)^2(n\theta^2\int_0^1{(t^{n-1} - 2t^n + t^{n+1})dt} - \frac{\theta^2}{(n+1)^2}) =
\theta^2(n(n+1)^2\cdot (\frac{t^n}{n} - 2\frac{t^{n+1}}{n+1} + \frac{t^{n+2}}{n+2})|_0^1 - 1) =
\theta^2(n(n+1)^2\cdot (\frac{1}{n} - \frac{2}{n+1} + \frac{1}{n+2}) - 1) =
\theta^2(\frac{2(n+1)}{n+2} - 1) =
\frac{n\theta^2}{n+2}$

$Var(\hat\theta_2) \underset{n \rightarrow +\infty}{\longrightarrow} \theta^2 \Rightarrow$ оценка несостоятельная

<br>

в) Сравнить оценки невозможно, так как одна из них не выполняет условие состоятельности, поэтому в данном случае $\hat\theta_1$ является оптимальной оценкой

<hr>'''),
            12:
                (r'''Пусть X – случайная величина, которая имеет равномерное распределение на отрезке [0, $\theta$]. Рассмотрим выборку объема 3 и класс оценок вида $\hat \theta = c \cdot X$ неизвестного параметра $\theta$. Найдите такое c, чтобы: a) оценка $\hat \theta$ – несмещенная; б) оценка $\hat \theta$ эффективная в рассматриваемом классе.''',
                 r'''а)
$E(\hat\theta) = cE(\overline X) = cE(X) = c\cdot \frac{0+\theta}{2} = \frac{c}{2}\theta$

Найдём $c$ из уравнения:

$E(\hat\theta) = \theta$

$\frac{c}{2}\theta = \theta$

$c = 2$ - при таком $c$ оценка $\hat\theta = 2\overline X$ несмещённая

<br>

б)
$\Delta = Var(\hat\theta) + (E(\hat\theta) - \theta)^2 =
c^2 Var(\overline X) + E^2(\hat\theta) - 2E(\hat\theta)\theta + \theta^2 =
\frac{c^2}{n}\cdot\frac{\theta^2}{12} + \frac{c^2}{4}\theta^2 - c\theta^2 + \theta^2 =
\theta^2 (\frac{5}{18}c^2 - c + 1)$

Т.к. $\theta^2 > 0$, то необходимо минимизировать $(\frac{5}{18}c^2 - c + 1)$. Это парабола с ветвями вверх, а значит минимум находится в вершине $-\frac{b}{2a}$:

$c^* = \frac{9}{5} \Rightarrow \hat\theta = \frac{9}{5}\overline X$ - такая оценка является эффективной в рассматриваемом классе

<hr>'''),
            13:
                (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка объема n из равномерного закона распределения на отрезке $[−\theta; \theta]$,
где $\theta$ > 0 – неизвестный параметр. В качестве оценки параметра $\theta^2$ рассмотрим статистику $\hat \theta = \frac {3}{n} (X^2_1 + X_2^2 + . . . + X^2_n)$. Является ли статистика $\hat \theta$ несмещенной оценкой параметра $\theta^2$? Является статистика $\sqrt {\hat \theta}$ несмещенной оценкой параметра $ \sqrt \theta^2 = \theta$? Ответ обосновать.''',
                 r'''$E(\hat\theta) \stackrel{\color{lightgreen}{независ.}}{=} \frac{3}{n}\cdot n \cdot E(X^2) = 3(Var(X) + E^2(X)) = 3 \frac{(2\theta)^2}{12} = \theta^2 \Rightarrow$ статистика $\hat\theta$ является несмещённой оценкой параметра $\theta^2$

<br>

Для следующего потребуется неравенство Йенсена:

$f(E(\cdot)) \leq E(f(\cdot))$

Так как корень строго выпуклая функция, то знак в нашем случае строгий

Имеем:

$E(\sqrt{\hat\theta}) = \sqrt{\frac{3}{n}}\cdot E(\sqrt{X_1^2 + ... + X_n^2}) >
\sqrt{\frac{3}{n}}\cdot \sqrt{E(X_1^2 + ... + E_n^2)} =
\sqrt 3 \cdot \sqrt{\frac{(2\theta)^2}{12}} = \theta$

То есть, $E(\sqrt{\hat\theta}) > \theta \neq \theta \Rightarrow$ оценка смещённая

<hr>'''),
            14:
                (r'''Пусть $Y_k = \beta{x_k} + \epsilon_k$, k = 1, . . . n, где $x_k$ – некоторые константы, а $\epsilon_k$ – независимые одинаково распределенные случайные величины, $\epsilon_k \sim N(0; \sigma^2)$. Является ли оценка $\hat β = \frac {\sum ^n_{k=1} Y_k}{\sum^n_{i=1} x_i}$ несмещенной оценкой параметра $\beta$? Ответ обосновать.''',
                 r'''$E(\hat\beta) = \frac{E(\sum_{k=1}^{n}{Y_k})}{E(\sum_{k=1}^{n}{x_k})} =
\frac{n\cdot E(Y)}{n\cdot E(x)} = \frac{E(\beta x + \varepsilon)}{x} =
\frac{\beta x + 0}{x} = \beta \Rightarrow$ оценка несмещённая

<hr>'''),
            15:
                (r'''Пусть $Y_k = \beta{x_k} + \epsilon_k$, k = 1, . . . n, где $x_k$ – некоторые константы, а $\epsilon_k$ – независимые одинаково распределенные случайные величины, $\epsilon_k \sim N(0; \sigma^2)$. Является ли оценка $\hat \beta =\frac {1}{n} \sum^n_{k=1}\frac {Y_k}{x_k}$ несмещенной оценкой параметра $\beta$? Ответ обосновать.''',
                 r'''$E(\hat\theta) = \frac{1}{n}E(\sum_{k=1}^n{\frac{Y_k}{x_k}}) = \frac{1}{n}\sum_{k=1}^n{\left(E(\frac{\beta x_k}{x_k}) + E(\frac{\varepsilon_k}{x_k})\right)} =
\frac{1}{n}\cdot n \frac{\beta x + 0}{x} = \beta \Rightarrow$ оценка несмещённая

<hr>'''),
            16:
                (r'''В таблице представлены данные по числу сделок на фондовой бирже за квартал для 400 инвесторов:

$\begin{array}{|c|c|}
\hline
x_i&0&1&2&3&4&5&6&7&8&9&10\\
\hline
n_i&146&97&73&34&23&10&6&3&3&3&2\\
\hline
\end{array}$

В предположении, что случайное число сделок описывается распределением Пуассона, оцените параметр $\lambda$ методом моментов. Определите вероятность того, что число сделок за квартал будет не
менее трех, применяя: а) метод моментов; б) непосредственно по таблице.''',
                 r'''$\nu_1 = E(X) = \lambda$

$\hat\nu_1 = \overline X$

По методу моментов $\nu_1 = \hat\nu_1$:

$\hat\lambda = \overline X$
```
x_arr = []

xi = np.arange(0, 11)
ni = [146, 97, 73, 34, 23, 10, 6, 3, 3, 3, 2]

for i in range(len(xi)):
    x_arr.extend([xi[i]] * ni[i])

x_arr = np.array(x_arr)

lambd = x_arr.mean()
lambd

# не менее трёх по методу моментов
poisson(lambd).sf(2)

# не менее трёх по таблице
sum(ni[3:]) / sum(ni)

```
<hr>'''),
            17:
                (r'''Пусть случайная величина X равномерно распределена на отрезке [0; 4$\theta$]. Найдите методом моментов оценку для параметра $\theta$. Является ли оценка а) несмещенной; б) состоятельной? Ответ обосновать.''',
                 r'''$\nu_1 = E(X) = \frac{0 + 4\theta}{2} = 2\theta$

$\hat\nu_1 = \overline X$

По методу моментов $\nu_1 = \hat\nu_1$:

$\hat\theta = \frac{\overline X}{2}$

<br>

а)
$E(\hat\theta) = \frac{1}{2}E(\overline X) = \frac{1}{2}E(X) = \frac{1}{2}\cdot \frac{4\theta}{2} = \theta \Rightarrow$ оценка несмещённая

<br>

б)
$Var(\hat\theta) = \frac{1}{4}Var(\overline X) = \frac{1}{4n}Var(X) =
\frac{1}{4n}\cdot\frac{(4\theta)^2}{12} = \frac{\theta^2}{3n}$

$Var(\hat\theta) \underset{n \rightarrow +\infty}{\longrightarrow} 0 \Rightarrow$ оценка состоятельная

<hr>'''),
            18:
                (r'''Пусть случайная величина X равномерно распределена на отрезке [a; b]. Найти методом моментов оценки для параметров a и b.''',
                 r'''$\nu_1 = E(X) = \frac{a+b}{2}$

$\nu_2 - \nu_1^2 = Var(X) = \frac{(b-a)^2}{2}$

$\hat\nu_k = \overline{X^k}$

Решим систему:

$\begin{cases}
E(X) = \overline X\\
Var(X) = \widehat{Var}(X)
\end{cases}$

$\begin{cases}
\frac{a+b}{2} = \overline X\\
\frac{(b-a)^2}{12} = \widehat{Var}(X)
\end{cases}$

Имеем: $a = 2\overline X - b$, тогда:

$\frac{(b - 2\overline X + b)^2}{12} = \widehat{Var}(X)$

$4(b - \overline X)^2 = 12\widehat{Var}(X)$

$b - \overline X = \sqrt{3\widehat{Var}(X)}$

Тогда:

$\begin{cases}
a = \overline X - \sqrt{3\widehat{Var}(X)}\\
b = \overline X + \sqrt{3\widehat{Var}(X)}
\end{cases}$

<hr>'''),
            19:
                (r'''Случайная величина X (срок службы изделия) имеет распределение, плотность которого задается формулой $f(x) = \lambda e^{−\lambda(x−\tau)}, x > \tau , \lambda > 0$.
В таблице приведены сгруппированные данные по срокам службы (в часах) для n = 423 изделий:

$\begin{array}{|c|c|}
\hline
x_i&4,55&11,55&18,55&25,55&32,55&39,55&46,55&53,55&60,55\\
\hline
n_i&219&98&50&25&17&7&2&4&1\\
\hline
\end{array}$

Найдите методом моментов точечные оценки неизвестных параметров $\lambda$ и $\tau$ распределения. Используя полученные оценки, оцените время, которое изделие прослужит с вероятностью 90,66%.

Ответ: $\hat\lambda = 0,0992; \hat\tau = 1,4873; T \approx 26,07$.''',
                 r'''
```
x_arr = []

xi = np.linspace(4, 60, 9) + 0.55
ni = [219, 98, 50, 25, 17, 7, 2, 4, 1]

for i in range(len(xi)):
    x_arr.extend([xi[i]] * ni[i])

x_arr = np.array(x_arr)

lambd, x, tau = sp.symbols('lambda, x, tau')
fx = lambd * sp.exp(-lambd * (x - tau))
nu1 = sp.integrate(x*fx, (x, tau, None)).args[0][0]
nu2 = sp.integrate(x**2*fx, (x, tau, None)).args[0][0]
nu1

nu2

nu1_hat = x_arr.mean()
nu2_hat = (x_arr ** 2).mean()

res = sp.solve([nu1_hat - nu1, nu2_hat - nu2], [lambd, tau])
res
```
Так как $\lambda > 0$, то подходит решение:
```
res[1]
```
$\hat\lambda = 0.0992$

$\hat\tau = 1.4873$
```
lambd_ = 0.0992
tau_ = 1.4873

expon(scale=1/lambd_, loc=tau_).ppf(0.9066)
```'''),
            20:
                (r'''Известно, что доля возвратов по кредитам в банке имеет распределение $F(x) = x^\beta, 0 \leq  x \leq 1$.
Наблюдения показали, что в среднем она составляет 78%. Методом моментов оцените параметр $\beta$ и вероятность того, что она опуститься ниже 67%.''',
                 r'''Найдём плотность:

$f(x) = F'(x) = \beta x^{\beta - 1}$

$\nu_1 = \int_0^1{x\cdot f(x) dx} = \int_0^1{\beta x^\beta} = \beta\cdot \frac{x^{\beta + 1}}{\beta + 1}|_0^1 = \frac{\beta}{\beta + 1}$

$\nu_1 = \hat\nu_1 \Rightarrow \frac{\beta}{\beta + 1} = \overline X$

По условию, $\overline X = 0.78$, тогда:

$\beta = 0.78\beta + 0.78$

$\beta = \frac{78}{22}$, $\beta = \frac{39}{11}$

Вероятность того, что опустится ниже 67%:

$P(X < 0.67) = F(0.67) = 0.67^{\frac{39}{11}}$
```
0.67 ** (39/11)
```'''),
            21:
                (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка объема n из распределения Пуассона с параметром $\lambda: P(X = k) = \frac {\lambda^ke^{−\lambda}}{k!}$, k = 0, 1, 2, . . . Найдите методом максимального правдоподобия по выборке $x_1, x_2, . . . , x_n$ точечную оценку неизвестного параметра $\lambda$ распределения Пуассона.''',
                 r'''Составим функцию правдоподобия:

$\large L = \frac{\lambda^{x_1}e^{-\lambda}}{x_1!}\cdot\ ...\ \cdot \frac{\lambda^{x_n}e^{-\lambda}}{x_n!}$

$\large L = e^{-\lambda n}\cdot\prod_{i=1}^n{\frac{\lambda^{x_i}}{x_i!}}$

$l = ln(L) = -\lambda n + \sum_{i=1}^{n}{(x_iln(\lambda) - ln(x_i!))}$

<br>

Приравняем производную к нулю для нахождения точки экстремума:

$l'_\lambda = -n + \sum_{i=1}^{n}{\frac{x_i}{\lambda}} = 0$

$\hat\lambda n = \sum_{i=1}^{n}{x_i}$

$\hat\lambda = \frac{1}{n}\sum_{i=1}^{n}{x_i} = \overline X$

<hr>'''),
            22:
                (r'''Найдите методом максимального правдоподобия по выборке $x_1, x_2, . . . , x_n$ точечную оценку $\hat \lambda$ неизвестного параметра $\lambda$ показательного закона распределения, плотность которого $f(x) = \lambda e^{−{\lambda}x}, x \geq 0$.''',
                 r'''Составим функцию правдоподобия:

$\large L = \lambda e^{-\lambda x_1} \cdot\ ...\ \cdot \lambda e^{-\lambda x_n}$

$\large L = \lambda^n e^{-\lambda \sum_{i=1}^n{x_i}}$

$l = ln(L) = n ln(\lambda) - \lambda \sum_{i=1}^n{x_i}$

<br>

Приравняем производную к нулю для нахождения точки экстремума:

$l'_\lambda = \frac{n}{\lambda} - \sum_{i=1}^{n}{x_i} = 0$

$\frac{1}{\hat\lambda} = \frac{1}{n}\sum_{i=1}^{n}{x_i} = \overline X$

$\hat\lambda = \frac{1}{\overline X}$

<hr>'''),
            23:
                (r'''Найдите оценки параметров a и b по методу максимального правдоподобия для равномерного распределения U([a, b]).''',
                 r'''$f(x) = \frac{1}{b-a}$, если $x \in [a, b]$; 0 иначе

Составим функцию правдоподобия:

$L = \frac{1}{b-a}\cdot\ ...\ \cdot \frac{1}{b-a} = \frac{1}{(b-a)^n}$

<br>

Максимизируем функцию:

$\frac{1}{(b-a)^n} \longrightarrow max$

$(b-a)^n \longrightarrow min$

$b-a \longrightarrow min$

$\begin{cases}
b \longrightarrow min\\
a \longrightarrow max
\end{cases}$

<br>

Имеем вариационный ряд по определению равномерного распределения:

$a \leq X_{(1)} \leq\ ...\ \leq X_{(n)} \leq b$

Тогда минимально возможная оценка для $b$ составит $\hat b = X_{(n)}$, а максимально возможная для $a$: $\hat a = X_{(1)}$

<hr>'''),
            24:
                (r'''Пусть $X_1, X_2, . . . , X_n$ – выборка из дискретного распределения $P(X = −1) = \theta, P(X = 1) = 4\theta, P(X = 2) = 2\theta, P(X = 0) = 1 − 7\theta, \theta \in (0; \frac {1}{7})$. Найдите оценку параметра $\theta$ по методу максимального правдоподобия. Является ли полученная оценка: а) несмещенной; б) состоятельной. Ответ обосновать.''',
                 r'''Составим функцию правдоподобия:

$ L(\vec x, \theta) = P_{\theta}(X=x_1) \cdot P_{\theta}(X=x_2) \cdot ... \cdot P_{\theta}(X=n)$

<br>

Пусть $n_1, n_2, n_3, n_4$ - количество значений $-1, 0, 1, 2$ в выборке соответственно. Заметим, что $n_1 + n_2 + n_3 + n_4 = n$.

Имеем:

$L = P_{\theta}(X=-1) ^ {n_1} \cdot P_{\theta}(X=0) ^ {n_2} \cdot P_{\theta}(X=1) ^ {n_3} \cdot P_{\theta}(X=2) ^ {n_4} = $
<br>
$ = \theta ^ {n_1} \cdot (1 - 7\theta) ^ {n_2} \cdot (4\theta) ^ {n_3} \cdot (2 \theta) ^ {n_4} = $
<br>
$ = 2 ^ {2n_3 + n_4} \cdot \theta ^ {n - n_2} \cdot (1 - 7\theta) ^ {n_2}$

<br>

$ ln(L) = l = (2 n_3 + n_4) \cdot ln(2) + (n - n_2) \cdot ln(\theta) + n_2 \cdot ln(1 - 7\theta)$

<br>

Приравняем производную к нулю для нахождения точки экстремума:

$ l_\theta' = \frac{n - n_2}{\theta} - \frac{7 n_2}{1 - 7\theta} = 0 $
<br>
$ \frac{n - n_2}{\hat{\theta}} = \frac{7n_2}{1 - 7\hat{\theta}} $
<br>
$ \frac{1 - 7\hat{\theta}}{\hat{\theta}} = \frac{7n_2}{n - n_2} $
<br>
$ \frac{1}{\hat{\theta}} - 7 = \frac{7n_2}{n - n_2} $
<br>
$ \frac{1}{\hat{\theta}} = \frac{7n_2 + 7n - 7n_2}{n - n_2} $
<br>
$ \hat{\theta} = \frac{n - n_2}{7n} $

<br>

а)
$E(\hat\theta) = E(\frac{n - n_2}{7n}) = \frac{1}{7} - \frac{1}{7n}E(n_2)$

Очевидно, $n_i \sim Bin(n, p = P(X = x_i)), E(n_i) = np, Var(n_i) = npq$

В нашем случае, $n_2 \sim Bin(n, p = 1 - 7\theta)$, тогда:

$E(\hat\theta) = \frac{1}{7} - \frac{1}{7n}\cdot n(1-7\theta) = \theta \Rightarrow$ оценка несмещённая

<br>

б)
$Var(\hat\theta) = \frac{1}{49n^2}Var(n_2) = \frac{1}{49n^2}\cdot n(1-7\theta)(1-1+7\theta) = \frac{\theta(1-7\theta)}{7n}$

$Var(\hat\theta) \underset{n \rightarrow +\infty}{\longrightarrow} 0 \Rightarrow$ оценка состоятельная

<hr>'''),
            25:
                (r'''Пусть $\hat f$ – оценка числа степеней свободы f вида $\hat f = \frac {(\frac {s^2_X}{n} + \frac {s^2_Y}{m})^2}{\frac {s^4_X}{n^2(n−1)} + \frac {s^4_Y}{m^2(m−1)}}$. Покажите, что $min(n - 1; m - 1) \leq \hat f \leq n + m - 2$.''',
                 r'''1) Пусть $min(n - 1; m - 1) = n - 1$, тогда:

$\frac {(\frac {s^2_X}{n} + \frac {s^2_Y}{m})^2}{\frac {s^4_X}{n^2(n−1)} + \frac {s^4_Y}{m^2(m−1)}} \geq n - 1$

$\frac {s^4_X}{n^2} + \frac {s^4_Y}{m^2} + 2\frac{s^2_X s^2_Y}{nm} \geq \frac {s^4_X}{n^2} + \frac {s^4_Y (n-1)}{m^2(m−1)}$

$\frac {s^2_Y}{m} + 2\frac{s^2_X}{n} \geq \frac {s^2_Y (n-1)}{m(m−1)}$

$\frac {s^2_Y}{m}(1 - \frac{n-1}{m-1}) + 2\frac{s^2_X}{n} \geq 0$

Очевидно, что $\frac {s^2_Y}{m} \geq 0$, $2 \frac {s^2_X}{n} \geq 0$

Так как $min(n - 1; m - 1) = n - 1$, то $n - 1 \leq m - 1$, а значит, $\frac{n-1}{m-1} \leq 1$ и $1 - \frac{n-1}{m-1} \geq 0$

Тогда сумма выражений $\geq 0$, больше либо равна нулю, что и показано в преобразованном выражении

<br>

2) Пусть $min(n - 1; m - 1) = m - 1$, тогда:

$\frac {(\frac {s^2_X}{n} + \frac {s^2_Y}{m})^2}{\frac {s^4_X}{n^2(n−1)} + \frac {s^4_Y}{m^2(m−1)}} \geq m - 1$

$\frac {s^4_X}{n^2} + \frac {s^4_Y}{m^2} + 2\frac{s^2_X s^2_Y}{nm} \geq \frac {s^4_X(m - 1)}{n^2(n-1)} + \frac {s^4_Y}{m^2}$

$\frac {s^2_X}{n} + 2\frac{s^2_Y}{m} \geq \frac {s^2_X(m - 1)}{n(n-1)}$

$\frac {s^2_X}{n}(1 - \frac{m-1}{n-1}) + 2\frac{s^2_Y}{m} \geq 0$

Очевидно, что $\frac {s^2_X}{n} \geq 0$, $2 \frac {s^2_Y}{m} \geq 0$

Так как $min(n - 1; m - 1) = m - 1$, то $m - 1 \leq n - 1$, а значит, $\frac{m-1}{n-1} \leq 1$ и $1 - \frac{m-1}{n-1} \geq 0$

Тогда сумма выражений $\geq 0$, больше либо равна нулю, что и показано в преобразованном выражении

<br>

3) Покажем максимум функции:

$\frac {(\frac {s^2_X}{n} + \frac {s^2_Y}{m})^2}{\frac {s^4_X}{n^2(n−1)} + \frac {s^4_Y}{m^2(m−1)}} \leq n + m - 2 = (n - 1) + (m - 1)$

$\frac {s^4_X}{n^2} + \frac {s^4_Y}{m^2} + 2\frac{s^2_X s^2_Y}{nm} \leq \frac{s^4_X}{n^2} + \frac {s^4_X(m - 1)}{n^2(n-1)} + \frac {s^4_Y(n - 1)}{m^2(m-1)} + \frac {s^4_Y}{m^2}$

$2\frac{s^2_X s^2_Y nm (n-1)(m-1)}{n^2m^2(n-1)(m-1)} \leq \frac {s^4_X(m - 1)^2m^2}{n^2m^2(n-1)(m-1)} + \frac {s^4_Y(n - 1)^2n^2}{n^2m^2(n-1)(m-1)}$

$\frac{\left(m(m-1)s^2_X - n(n - 1)s^2_Y\right)^2}{n^2m^2(n-1)(m-1)} \geq 0$

Выражение верно $\forall m > 1, n > 1, s^2_X, s^2_Y$

<br>

4) Покажем максимум функции через производную:

Пусть $\hat{\theta} = \frac{s_X^2}{s_Y^2}$, тогда

$\hat{df} = \frac{(\frac{s_X^2}{n} + \frac{s_Y^2}{m})^2}{\frac{s^4_X}{n^2(n-1)} + \frac{s^4_Y}{m^2(m-1)}}=
 \frac{(\hat{\theta} + \frac{n}{m})^2}{\frac{1}{n-1} \cdot \hat{\theta^2} + \frac{1}{m-1} \cdot (\frac{n}{m})^2}$

Найдя производную по $\hat{\theta}$ получим:
<br>
$\frac{\partial \hat{df}}{\partial \hat{\theta}} =
\frac{2m(m-1)(n-1)(m\hat{\theta} +n)(m^2\hat{\theta}^2(m-1) - m\hat{\theta}(m-1)(m\hat{\theta}+n)+n^2(n-1))}
{(m^2\hat{\theta}^2(m-1)+n^2(n-1))^2}$
<br>
Приравняв её к нулю, получим:
<br>
$ \hat{\theta} = \frac{n\cdot(n - 1)}{m\cdot(m - 1)} $
<br>
Подставим полученное значение в исходную формулу:
<br>
$ \hat{df} =
 \frac{(\hat{\theta} + \frac{n}{m})^2}{\frac{1}{n-1} \cdot \hat{\theta^2} + \frac{1}{m-1} \cdot (\frac{n}{m})^2}
=  \frac{(\frac{n\cdot(n - 1)}{m\cdot(m - 1)} + \frac{n}{m})^2}{\frac{1}{n-1} \cdot (\frac{n\cdot(n - 1)}{m\cdot(m - 1)})^2 + \frac{1}{m-1} \cdot (\frac{n}{m})^2}
= \frac{\frac{n^2\cdot(n + m - 2)^2}{m^2\cdot(m - 1)^2}}{\frac{n^2\cdot(n - 1)}{m^2\cdot(m - 1)^2} + \frac{n^2}{m^2(m-1)}}
= \frac{\frac{n^2\cdot(n + m - 2)^2}{m^2\cdot(m - 1)^2}}{\frac{n^2\cdot(n + m - 2)}{m^2\cdot(m - 1)^2}}
= n + m - 2
$

<br>

Код в питоне:
<br>
```
t, n, m = sp.symbols('theta n m')
eq = (t + n/m)**2 / (1/(n-1) * t**2 + 1/(m-1) * (n/m)**2)
der = sp.Derivative(eq, t).simplify().simplify()
sp.solve(der, t)
```
<hr>'''),
            26:
                (r'''Пусть $f_{\alpha}(1; m)$ – (верхняя) процентная точка распределения Фишера с 1 и m степенями свободы, $t_{\frac {\alpha}{2}}
(m)$ – (верхняя) процентная точка распределения Стьюдента с m степенями свободы. Покажите,
что $f_\alpha(1; m) = t^2_{\frac{\alpha}{2}}(m)$.''',
                 r'''Хи-квадрат: $\chi^2_n = \sum_{i=1}^{n}{Z^2_i}$, где $Z \sim N(0, 1)$

Распределение Фишера: $\Large \mathbb F(n, m) = \frac{\frac{\chi^2_n}{n}}{\frac{\chi^2_m}{m}}$

Распределение Стьюдента: $\Large T(n) = \frac{Z}{\sqrt{\frac{\chi^2_n}{n}}}$

Определение верхней процентной точки: $P(X > x_\alpha) = \alpha$

Свойство верхней процентной точки распр. Стьюдента: $t_{1 - \alpha}(k) = -t_\alpha(k)$

<br>

**Решение**

Возведём распр. Стьюдента в квадрат:

$\Large T^2(m) = \frac{Z^2}{\frac{\chi^2_m}{m}} = \frac{\frac{\chi^2_1}{1}}{\frac{\chi^2_m}{m}} = \mathbb F(1, m)$

Рассмотрим верхнюю процентную точку распределения Фишера по определению:

$P(F > f_\alpha) = \alpha$

По доказанному:

$P(T^2 > f_\alpha) = \alpha$

Из условия:

$P(T^2 > t^2_{\frac{\alpha}{2}}) = \alpha$

$P(|T| > |t_{\frac{\alpha}{2}}|) = \alpha$

$P(T < -t_{\frac{\alpha}{2}}) + P(T > t_{\frac{\alpha}{2}}) = \alpha$

Используя свойство верхней процентной точки:

$P(T < t_{1 - \frac{\alpha}{2}}) + P(T > t_{\frac{\alpha}{2}}) = \alpha$

$1 - P(T > t_{1 - \frac{\alpha}{2}}) + P(T > t_{\frac{\alpha}{2}}) = \alpha$

Обратно по определению верхней процентной точки:

$1 - 1 + \frac{\alpha}{2} + \frac{\alpha}{2} = \alpha$ - тождество, а значит $f_α(1; m) = t^2_{\frac{α}{2}}(m)$ верно

<hr>'''),
            27:
                (r'''Инвестор наблюдает за колебаниями котировок акций компаний A и B в течение 100 торговых дней (по закрытию торгов). В результате наблюдений получена следующая статистика: количество дней, когда обе котировки падали – 26;обе котировки росли – 25; котировки падали, а котировки при этом росли – 29; наоборот, котировки росли, а котировки падали – 20. При 1% -м уровне значимости проверьте гипотезу о равновероятности указанных четырех комбинаций падения и роста.''',
                 r'''Необходимо проверить нулевую гипотезу:

$H_0: p_{uu} = p_{ud} = p_{du} = p_{dd} = 0.25$

Проверим с помощью критерия согласия $\chi^2$-Пирсона:

$\chi^2_П = \sum_{i=1}^{l}{\frac{(v_i - np_i) ^ 2}{np_i}}$
```
n = 100
v = np.array([26, 25, 29, 20])

p = np.array([0.25] * 4)

l = 4

alpha = 0.01

chiP = np.sum((v - n * p) ** 2/(n * p))
chiP

chi2a = chi2(l - 1).isf(alpha)
chi2a
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \chi^2_П > \chi^2_\alpha(l - 1)\}$

В нашем случае:

$K_{0.01} = (11.3449; +\infty)$

<br>

$\chi^2_П = 1.68 \notin K_{0.01} \Rightarrow H_0$ не отвергается
```
# p-value для умных:

pv = chi2(l - 1).sf(chiP)
pv

# в одну строчку:

chisquare(v, p * n)
```
<hr>'''),
            28:
                (r'''В десятичной записи числа $\pi$ среди 10 002 первых десятичных знаков после запятой цифры 0; 1; . . . ; 9 встречаются соответственно 968; 1026; 1021; 974; 1012; 1047; 1022; 970; 948; 1014 раз. На 5%-ом уровне значимости проверить гипотезу о равновероятности «случайных» чисел 0; 1; . . . ; 9, т.е. согласуются ли данные с гипотезой $H_0 : p_0 = p_1 = . . . p_9 = \frac {1}{10}$? Найдите P-значение критерия.''',
                 r'''Необходимо проверить нулевую гипотезу:

$H_0: p_0 = p_1 = ... = p_9 = 0.1$

Проверим с помощью критерия согласия $\chi^2$-Пирсона:

$\chi^2_П = \sum_{i=1}^{l}{\frac{(v_i - np_i) ^ 2}{np_i}}$
```
n = 10002
v = np.array([968, 1026, 1021, 974, 1012, 1047, 1022, 970, 948, 1014])

p = np.array([0.1] * 10)

l = 10
alpha = 0.05

chiP = np.sum((v - n * p) ** 2/(n * p))
chiP

chi2a = chi2(l - 1).isf(alpha)
chi2a
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \chi^2_П > \chi^2_\alpha(l - 1)\}$

В нашем случае:

$K_{0.05} = (16.91897; +\infty)$

<br>

$\chi^2_П = 9.4517 \notin K_{0.05} \Rightarrow H_0$ не отвергается

Рассчитаем p-value:
```
$PV(\vec{z}) = \mathbb P_{H_0} (\chi^2 > \chi^2_П)$


pv = chi2(l - 1).sf(chiP)
pv

# в одну строчку:

chisquare(v, p * n)
```
<hr>'''),
            29:
                (r'''Среди 10 000 «случайных чисел» 0,1, . . . , 9, числа, не превосходящие 4, встретились k = 5089 раз. Проверить на уровне значимости $\alpha$ = 0, 1, согласуются ли эти данные с гипотезой $H_0$ о равновероятности чисел. При каком уровне значимости эта гипотеза отвергается.''',
                 r'''Необходимо проверить нулевую гипотезу:

$H_0: p_{\leq 4} = p_{>4} = 0.5$

Проверим с помощью критерия согласия $\chi^2$-Пирсона:

$\chi^2_П = \sum_{i=1}^{l}{\frac{(v_i - np_i) ^ 2}{np_i}}$
```
n = 10000
v = np.array([5089, 10000 - 5089])

p = np.array([0.5] * 2)

l = 2

alpha = 0.1

chiP = np.sum((v - n * p) ** 2/(n * p))
chiP

chi2a = chi2(l - 1).isf(alpha)
chi2a
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \chi^2_П > \chi^2_\alpha(l - 1)\}$

В нашем случае:

$K_{0.1} = (2.7055; +\infty)$

<br>

$\chi^2_П = 3.1684 \in K_{0.1} \Rightarrow H_0$ отвергается

Рассчитаем p-value:

$PV(\vec{z}) = \mathbb P_{H_0} (\chi^2 > \chi^2_П)$
```
pv = chi2(l - 1).sf(chiP)
pv
```
При уровне значимости $\alpha > 0.075076$ гипотеза отвергается
```
# в одну строчку:

chisquare(v, p * n)
```
<hr>'''),
            30:
                (r'''При 8002 независимых испытаний события A, B и C, составляющие полную группу, осуществились 2014, 5008 и 980 раз соответственно. Верна ли на уровне значимости 0, 05 гипотеза $p(A) = 0, 5 - 2\theta ; p(B) = 0, 5 + \theta; p(C) = \theta (0 < \theta < 0, 25)$?''',
                 r'''Необходимо проверить нулевую гипотезу:

$H_0: p(A) = 0.5 - 2\theta; p(B) = 0.5 + \theta; p(C) = \theta; (0 < \theta < 0.25)$

Проверим с помощью критерия согласия $\chi^2$-Фишера:

$\chi^2_Ф = \sum_{i=1}^{l}{\frac{(v_i - np_i(\vec{x})) ^ 2}{np_i(\vec{x})}}$
```
theta = sp.symbols('theta')

v = np.array([2014, 5008, 980])

n = sum(v)

p = np.array([0.5 - 2 * theta, 0.5 + theta, theta])

l = 3

alpha = 0.05

chiF = np.sum((v - n * p) ** 2 / (n * p))

chiF
```
Для нахождения оптимальной оценки воспользуемся:

$\chi^2_\Phi \rightarrow min$

Для этого приравняем производную к нулю и найдём экстремум, подходящий под условие $0 < \theta < 0.25$
```
sp.solve(sp.Derivative(chiF, theta, evaluate=True), theta)
```
Таким образом, $\hat\theta = 0.1237$, тогда:
```
f = sp.lambdify(theta, chiF)
chiF_ = f(0.123730042643424)
chiF_

chi2a = chi2(l - 1 - 1).isf(alpha)
chi2a
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \chi^2_Ф > \chi^2_\alpha(l - 1 - m)\}$

В нашем случае:

$K_{0.05} = (3.8414; +\infty)$

<br>

$\chi^2_Ф = 0.1831 \notin K_{0.05} \Rightarrow H_0$ не отвергается
```
# p-value для умных

pv = chi2(l - 1 - 1).sf(chiF_)
pv

# в одну строчку после нахождения теты

chisquare(v, n * np.array([0.5 - 2 * 0.12371709, 0.5 + 0.12371709, 0.12371709]), ddof=1)
```
'''),
            31:
                (r'''Пусть таблица сопряженности двух признаков имеет вид

\begin{array}{c|c|c}
&Y = y1&Y = y2\\
\hline
X = x1&a&b\\
\hline
X = x2&c&d\\
\end{array}

Показать, что статистика критерия $\chi^2$ Пирсона для проверки гипотезы независимости X и Y можно найти по формуле

$\chi^2 = \frac {n(ad − bc)^2}{(a + b)(a + c)(b + d)(c + d)}$''',
                 r'''Общая формула критерия Пирсона
$ \chi^2 = n \cdot \left[ \sum_{i=1}^{k} \sum_{j=1}^{m} (\frac{v_{ij}^2}{\alpha_i \beta_j}) - 1 \right], $

где $ {\alpha_i \beta_j} $ это суммы по строкам и столбцам соответсвенно

Последовательно распишем имеющиеся суммы для исходной формулы:

$ n \cdot \left[ \frac{a^2}{(a + b)(a + c)} + \frac{b^2}{(a + b)(b + d)} + \frac{c^2}{(a + c)(c + d)} + \frac{d^2}{(b + d)(c + d)} - 1 \right]$

Приведя всё к одному знаменателю и затем приведя подобные слагаемые (см. ниже), получим нужную нам форму:

$ n \cdot \left[\frac{a^2d^2 - 2abcd + b^2c^2}{(a+c)(a+b)(b+d)(c+d)} \right] = \frac{n(ad - bc)^2}{(a+c)(a+b)(b+d)(c+d)}$
```
a, b, c ,d = sp.symbols('a b c d')

exp1 = (a**2*(c+d)*(b+d)).expand()
exp1

exp2 = (b**2*(a+c)*(c+d)).expand()
exp2

exp3 = (c**2*(a+b)*(b+d)).expand()
exp3

exp4 = (d**2*(a+c)*(a+b)).expand()
exp4

exp1 + exp2 + exp3 + exp4 - ((a+c)*(a+b)*(b+d)*(c+d)).expand()
```
'''),
            32:
                (r'''Число $\pi$ до 30 знака после запятой имеет вид:

3, 141592653589793238462643383279.

Число $e$ до 30 знака после запятой имеет вид:

2, 718281828459045235360287471352.

Используя критерий однородности $\chi^2$,проверьте на уровне значимости $\alpha$ = 0, 05 гипотезу $H_0$ о том, что последовательности цифр после запятой для обоих чисел принадлежат одной генеральной совокупности.''',
                 r'''Необходимо проверить нулевую гипотезу:

$H_0: p_{i1} = p_{i2}\ \forall i \in [1; l]$

Для проверки воспользуется критерием однородности:

$\large \chi^2_О = n_1n_2\sum_{i=1}^{l}{\frac{1}{v_{i1} + v_{i2}}(\frac{v_{i1}}{n_1} - \frac{v_{i2}}{n_2})^2}$
```
n1 = n2 = 30
n = np.array([n1, n2])

X = list(map(int, list('141592653589793238462643383279')))
Y = list(map(int, list('718281828459045235360287471352')))
v1 = np.array([X.count(i) for i in range(10)])
v2 = np.array([Y.count(i) for i in range(10)])
v = np.array([v1, v2])

l = 10

alpha = 0.05

chio = n1 * n2 * np.sum(1 / (v1 + v2) * (v1 / n1 - v2 / n2) ** 2)
chio

chia = chi2((l - 1)).isf(alpha)
chia
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \chi^2_О > \chi^2_\alpha(l - 1)\}$

В нашем случае:

$K_{0.05} = (16.9189; +\infty)$

<br>

$\chi^2_О = 6.9539 \notin K_{0.05} \Rightarrow H_0$ не отвергается
```
# для умных

pv = chi2(l - 1).sf(chio)
pv

# в одноу строчку

contingency.chi2_contingency(np.vstack([v1, v2]).T)
```
<hr>'''),
            33:
                (r'''Из таблицы случайных чисел выбрано n = 150 двузначных чисел. Частоты $n_i$ чисел, попавших в интервал [10i; 10i + 9],(i = 0, 1, . . . , 9) равны: (16; 15; 19; 13; 14; 19; 14; 11; 13; 16). Проверить, используя критерий Колмогорова, гипотезу $H_0$ о согласии выборки с законом равномерного распределения.
Уровень значимости $\alpha$ принять равным 0, 01.''',
                 r'''Необходимо проверить нулевую гипотезу:

$H_0: F(X) = F_U(X)$

Для этого вычислим следующую статистику:

$D_n = \underset{x\in(-\infty; +\infty)}{sup}|\hat F_n(x) - F(x)|$

Её можно вычислить как:

$D^+_n = \underset{1\leq k\leq n}{max}\left\{\frac k n - F_U(X_{(k)})\right\}$

$D^-_n = \underset{1\leq k\leq n}{max}\left\{F_U(X_{(k)}) - \frac{k - 1}{n}\right\}$

$D_n = \sqrt{n}\cdot max\{D^+_n; D^-_n\}$
```
N = 150
alpha = 0.01

v = [16, 15, 19, 13, 14, 19, 14, 11, 13, 16]

X = uniform(10, 89)

n = len(v)
k = np.arange(n) + 1
x = X.cdf(v)
x.sort()

D_plu = max(k/n - x)

D_min = max(x - (k-1)/n)

D = max(D_min, D_plu) * np.sqrt(n)
D

ca = kstwobign.isf(alpha)
ca
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \sqrt n \cdot D_n > c_\alpha\}$

В нашем случае:

$K_{0.01} = (1.6276; +\infty)$

<br>

$\sqrt n \cdot D_n = 2.8425 \in K_{0.01} \Rightarrow H_0$ отвергается
```
# pvalue для умных

pv = kstwo(n).sf(D / np.sqrt(n))
pv

# в одну строчку

kstest(rvs=v, cdf=X.cdf)
```
<hr>'''),
            34:
                (r'''Число $\pi$ до 30 знака после запятой имеет вид:

3, 141592653589793238462643383279.

Число $e$ до 30 знака после запятой имеет вид:

2, 718281828459045235360287471352.

Используя критерий однородности Колмогорова–Смиронова, проверьте на уровне значимости α = 0, 05 гипотезу H0 о том, что последовательности цифр после запятой для обоих чисел принадлежат
одной генеральной совокупности.''',
                 r'''Используем следующую статистику:
$ \frac{n \cdot m}{n + m} \cdot D$, где D - максимальное расстояние между эмпирическими функциями распределений

Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \frac{n \cdot m}{n + m} \cdot D > c_\alpha\}$

В нашем случае:

$K_{0,05} = (1,358; +\infty)$

<br>

$\sqrt n \cdot D_n = 0,5164 \notin K_{0.05} \Rightarrow H_0$ не отвергается
```
group = np.arange(10)
X = list(map(int, list('141592653589793238462643383279')))
Y = list(map(int, list('718281828459045235360287471352')))
alpha = 0.05
n = list(map(len, [X, Y]))
N = sum(n)
c = kstwobign.isf(alpha)

frequency_X = np.array([X.count(i) for i in range(10)])
frequency_Y = np.array([Y.count(i) for i in range(10)])

total = sum(frequency_X)
edf_X = [sum(frequency_X[:i+1])/total for i in range(len(frequency_X))]

total = sum(frequency_Y)
edf_Y = [sum(frequency_Y[:i+1])/total for i in range(len(frequency_Y))]

# 1 способ
# так как значения функции распределния принимают одинаковые, просто максимальная разница по модулю
sup = max(abs(np.array(edf_Y) - np.array(edf_X)))
sup

# 2 способ
# умнота из лекций
sup = max(abs(np.array(edf_Y) - np.array(edf_X)))
sup

# соединяем распределения
Z = [(val, 1) for val in X] + [(val, 0) for val in Y]
Z.sort(key = lambda x: x[0])
Z = np.array(Z)

#умная статистика
res = []
for j in range(1, N + 1):
    res.append(j*n[0]/N - np.sum(Z[:j][:, 1]))

D = N/(np.prod(n)) * max(res)
D

# а значит H_0 не отвергается
np.sqrt(np.prod(n)/np.sum(n)) * D > c

pv = kstwobign.sf(np.sqrt((n[0]*n[1])/(n[0]+n[1])) * D)
pv

ks_2samp(X, Y, mode='exact')

#асимптотическое pv (совпадает с библиотечным)
pv = kstwo.sf(D, np.round((n[0]*n[1])/(n[0]+n[1])))
pv

ks_2samp(X, Y, mode='asymp')
```
'''),
            35:
                (r'''Случайная выборка из 395 человек была разделена по возрастному признаку, а также по тому, переключают ли люди телевизионные каналы во время просмотра передачи. Данные исследования представлены в следующей таблице:

\begin{array}{|c|c|c|}
\hline
Переключение / Возраст&18–24&25–34&35–49&50–64\\
\hline
Да&60&54&46&41\\
\hline
Нет&40&44&53&57\\
\hline
\end{array}

Используя приведенные данные, проверьте гипотезу о том, что переключение каналов и возраст являются независмимыми признаками в случае, когда a) $\alpha$ = 5%; б) $\alpha$ = 2, 5%. Найдите P-значение
критерия.''',
                 r'''Решение при k = 2:
```
#дана таблица сопряжённости, а не данные!

n = 395
alpha = 0.05
k = 2 #значений X то есть переключат или нет
m = 4 #значений Y, то группа возраста

v = np.array([60, 54, 46, 41, 40, 44, 53, 57]).reshape(k, m)

alphas = np.sum(v, axis=1)
bettas = np.sum(v, axis=0)

res = 0
for i in range(k):
    for j in range(m):
        res += v[i, j]**2/(alphas[i]*bettas[j])

chiH = n*(res - 1)
chiH

chi2a = chi2((k-1)*(m-1)).isf(alpha)
chi2a

pv = chi2((k-1)*(m-1)).sf(chiH)
pv
```
Необходимо проверить нулевую гипотезу:

$H_0: p_{i1} = p_{i2}\ \forall i \in [1; l]$

Для проверки воспользуется критерием однородности:

$\large \chi^2_О = n_1n_2\sum_{i=1}^{l}{\frac{1}{v_{i1} + v_{i2}}(\frac{v_{i1}}{n_1} - \frac{v_{i2}}{n_2})^2}$
```
n = 395
alpha = 0.05
l = 4

v = np.array([60, 54, 46, 41, 40, 44, 53, 57]).reshape(k, m)

n1 = sum(v[0])
n2 = sum(v[1])
v1 = v[0]
v2 = v[1]

chio = n1 * n2 * np.sum(1 / (v1 + v2) * (v1 / n1 - v2 / n2) ** 2)
chio

chia = chi2(l - 1).isf(alpha)
chia
```
Критическая область имеет вид:

$K_\alpha = \{(x_1, ... x_n): \chi^2_О > \chi^2_\alpha(l - 1)\}$

В нашем случае:

$K_{0.05} = (7.8147; +\infty)$

<br>

$\chi^2_О = 8.006 \in K_{0.05} \Rightarrow H_0$ отвергается
```
chi2a = chi2(l - 1).isf(alpha / 2)
chi2a
```
$K_{0.025} = (9.3484; +\infty)$

<br>

$\chi^2_О = 8.006 \notin K_{0.025} \Rightarrow H_0$ не отвергается

Рассчитаем p-value:

$PV(\vec{z}) = \mathbb P_{H_0} (\chi^2 > \chi^2_О)$
```
pv = chi2(l - 1).sf(chio)
pv
# в одну строчку

contingency.chi2_contingency(v)
```
<hr>''')
        },
        "Q4": {
            1:
                (r'''В первом броске участвуют 160 несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал орел. Известно, что вероятность выпадения орла для данных несимметричных монет равна 0,55. найдите 1) математическое ожидание числа орлов, выпавших во втором броске 2) дисперсию условного математического ожидания числа орлов, выпавших во втором броске, относительно числа орлов, выпавших в первом броске.
''',
                r'''Пусть $X$ - монета, $S$ - сумма монет, $N$ - выпавшее число нужных монет

<hr>

$E(X) = p$

$Var(X) = p\cdot q$

$E(N) = n\cdot p$ (биномиальная СВ)

$Var(N) = n\cdot p\cdot q$

<hr>

Свойства:

$E(X) = E(E(X|Y))$

$Var(X) = E(Var(X|Y)) + Var(E(X|Y))$

<hr>

Для заданий:

* $E(S|N) = E(X_1 + X_2 + ... + X_N | N) = E(X_1) + ... + E(X_N) = E(X) \cdot N \Rightarrow \color{orange}{E(E(S|N))} = E(N\cdot E(X)) = \color{orange}{E(N)\cdot E(X)}$

<br>

* $\color{orange}{E(Var(S|N))} = E(Var(X_1) + ... + Var(X_N)) = E(N\cdot Var(X)) = \color{orange}{Var(X) \cdot E(N)}$ (можем вынести $Var(X)$ т.к. не является СВ)

<br>

* $\color{orange}{Var(E(S|N))} = Var(E(X)\cdot N) = \color{orange}{E^2(X)\cdot Var(N)}$
```

n = 160
p = 0.55

E_coin = p
Var_coin = p * (1-p)


E_bin = n * p
Var_bin = n * p * (1-p)
ans1 = E_coin * E_bin

E_Var__S_N = Var_coin * E_bin
Var_E__S_N = E_coin**2 * Var_bin
ans2 = Var_E__S_N

answer(ans1, ans2)
```
'''),
            2:
                (r'''В первом броске участвуют 79 несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал орел. Известно, что вероятность выпадения орла для несимметричных монет равна 0,6. Найдите 1) математическое ожидание числа орлов, выпавших во втором броске. 2) математическое ожидание условной дисперсии числа орлов, выпавших во втором броске, относительно числа орлов, выпавших в первом броске.''',
                 r'''
```
n = 79
p = 0.6

E_coin = p
Var_coin = p * (1-p)

E_bin = n * p
Var_bin = n * p * (1-p)
ans1 = E_coin * E_bin

E_Var__S_N = Var_coin * E_bin
Var_E__S_N = E_coin**2 * Var_bin
ans2 = E_Var__S_N

answer(ans1, ans2)
```'''),
            3:
                (r'''В первом броске участвуют 88 несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал "орел". Известно, что вероятность выпадения "орла" для данных несимметричных монет равна 0,7. Найдите: 1) математическое ожидание условной дисперсии числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске; 2) дисперсию условного математического ожидания числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске.''',
                 r'''
```
n = 88
p = 0.7

E_coin = p
Var_coin = p * (1-p)

E_bin = n * p
Var_bin = n * p * (1-p)
E_Var__S_N = Var_coin * E_bin
Var_E__S_N = E_coin**2 * Var_bin

answer(E_Var__S_N, Var_E__S_N)
```'''),
            4:
                (r'''Средний ущерб от одного пожара составляет 4,4 млн. руб. Предполагается, что ущерб распределен по показательному закону, а число пожаров за год - по закону Пуассона. Также известно, что за 5 лет в среднем происходит 14 пожаров. Найдите: 1) математическое ожидание суммарного ущерба от всех пожаров за один год; 2) стандартное отклонение суммарного ущерба от пожаров за год.''',
                 r'''Показательный закон:

$E(X) = \frac{1}{\lambda_{exp}}$

$Var(X) = \frac{1}{\lambda^2_{exp}}$

<hr>

Закон Пуассона:

$E(X) = Var(X) = \lambda_{pua}$

<hr>

Свойства:

$E(X) = E(E(X|Y))$

$Var(X) = E(Var(X|Y)) + Var(E(X|Y))$

<hr>

Для заданий:

Пусть $S$ - сумма ущерба, $X$ - ущерб, $N$ - количество пожаров

$\lambda_{exp} = \frac{1}{E(X)}$

$\lambda_{pua} = E(N) = \frac{количество.пожаров}{количество.лет}$

* $E(S|N) = E(X_1 + X_2 + ... + X_N | N) = E(X_1) + ... + E(X_N) = E(X) \cdot N \Rightarrow \color{orange}{E(E(S|N))} = E(N\cdot E(X)) = E(N) \cdot E(X) = \color{orange}{\lambda_{pua}\cdot E(X)}$

<br>

* $E(Var(S|N)) = E(Var(X_1) + ... + Var(X_N)) = E(N\cdot Var(X)) = Var(X) \cdot E(N) = \lambda_{pua} \cdot \frac{1}{\lambda^2_{exp}}$

<br>

* $Var(E(S|N)) = Var(E(X)\cdot N) = E^2(X)\cdot Var(N)= \lambda_{pua} \cdot \frac{1}{\lambda^2_{exp}}$

<br>

* $\color{orange}{std(S) = \sqrt{Var(S)} = \sqrt{E(Var(S|N)) + Var(E(S|N))} = \sqrt{2\lambda_{pua}\frac{1}{\lambda^2_{exp}}}}$
```

exp_mean = 4.4
year = 5
quant = 14

lambda_exp = 1/exp_mean
lambda_pua = quant/year

ans1 = lambda_pua * exp_mean

E_Var__S_N = lambda_pua * (1/lambda_exp) ** 2
Var_E__S_N = lambda_pua * (1/lambda_exp) ** 2

ans2 = np.sqrt(E_Var__S_N + Var_E__S_N)

answer(ans1, ans2)
```'''),
            5:
                (r'''Максимальный ущерб от страхового случая составляет 3,3 млн. руб. Предполагается, что фактический ущерб распределен равномерно от 0 до максимального ущерба, а число страховых случаев за год - по закону Пуассона. Также известно, что за 10 лет в среднем происходит 12 страховых случаев. Найдите: 1) математическое ожидание суммарного ущерба от всех страховых случаев за один год; 2) стандартное отклонение суммарного ущерба от страховых случаев за год.''',
                 r'''Равномерный закон:

$E(X) = \frac{a+b}{2}$

$Var(X) = \frac{(a+b)^2}{12}$

<hr>

Закон Пуассона:

$E(X) = Var(X) = \lambda_{pua}$

<hr>

Свойства:

$E(X) = E(E(X|Y))$

$Var(X) = E(Var(X|Y)) + Var(E(X|Y))$

<hr>

Для заданий:

Пусть $S$ - сумма ущерба, $X$ - ущерб, $N$ - количество пожаров

$\lambda_{pua} = E(N) = \frac{количество.пожаров}{количество.лет}$

* $E(S|N) = E(X_1 + X_2 + ... + X_N | N) = E(X_1) + ... + E(X_N) = E(X) \cdot N \Rightarrow \color{orange}{E(E(S|N))} = E(N\cdot E(X)) = E(N) \cdot E(X) = \color{orange}{\lambda_{pua}\cdot E(X)}$

<br>

* $E(Var(S|N)) = E(Var(X_1) + ... + Var(X_N)) = E(N\cdot Var(X)) = Var(X) \cdot E(N) = \lambda_{pua} \cdot Var(X)$

<br>

* $Var(E(S|N)) = Var(E(X)\cdot N) = E^2(X)\cdot Var(N)= \lambda_{pua} \cdot E^2(X)$

<br>

* $\color{orange}{std(S) = \sqrt{Var(S)} = \sqrt{E(Var(S|N)) + Var(E(S|N))} = \sqrt{\lambda_{pua}\cdot Var(X) + \lambda_{pua} \cdot E^2(X)}}$
```

b = 3.3
quant = 12
year = 10

E_damage = b / 2
Var_damage = b ** 2 / 12

lambda_pua = quant / year

ans1 = lambda_pua * E_damage

E_Var__S_N = lambda_pua * Var_damage
Var_E__S_N = lambda_pua * E_damage ** 2

ans2 = np.sqrt(E_Var__S_N + Var_E__S_N)

answer(ans1, ans2)
```'''),
            6:
                (r'''Для случайной цены Y
 известны вероятности: $P(Y=2)=0,6$
 и $P(Y=15)=0,4$
. При условии, что $Y=y$
, распределение выручки X
 является равномерным на отрезке $[0,7y]$
. Найдите: 1) математическое ожидание $E(XY)$
; 2) ковариацию $Cov(X,Y)$
.''',
                 r'''Равномерный закон:

$E(X) = \frac{a+b}{2}$

<hr>

Для задания:

$E(X) = E(E(X|Y)) = E(\frac{0 + 7Y}{2}) = \frac{7E(Y)}{2}$

$E(XY) = E(E(XY|Y)) = E(E(XY|Y=2) \cdot P(Y=2) + E(XY|Y=15) \cdot P(Y=15)) = $

$ = E(E(2X) \cdot P_2 + E(15X) \cdot P_{15}) $
$ = 2 \cdot P_2 \cdot E(X |Y=2) + 15 \cdot P_{15} \cdot E(X |Y=15) $

$\color{orange}{Cov(X, Y) = E(XY) - E(X)\cdot E(Y)}$
```
k = 7
prob = [0.6, 0.4]
values = [2, 15]

Y = rv_discrete(values=(values, prob))

X_mean = 0
for p, v in zip(prob, values):
    X_mean += p * v * k / 2

#E(XY) = E(E(XY|Y)) = E(E(XY|Y=2)*P(Y=2) + E(XY|Y=15)*P(Y=15))
XY_mean = 0
for p, v in zip(prob, values):
    XY_mean += p * v**2 * k / 2

ans2 = XY_mean - Y.mean() * X_mean

answer(XY_mean, ans2)

prob = [0.6, 0.4]
values = [2, 15]

Y = rv_discrete(values=(values, prob))

X_mean = 7 * Y.mean() / 2

# Var(Y) = E(Y^2) - E(Y)^2 => E(Y^2) = Var(Y) + E(Y)^2
XY_mean = 7 * (Y.var() + Y.mean() ** 2) / 2

ans2 = XY_mean - Y.mean() * X_mean

answer(XY_mean, ans2)
```'''),
            7:
                (r'''Игральная кость и 29
 монет подбрасываются до тех пор, пока в очередном броске не выпадет ровно 8
 "орлов". Пусть S
 – суммарное число очков, выпавших на игральной кости при всех бросках. Найдите: 1) математическое ожидание $E(S)$
; 2) стандартное отклонение $σ_S$
.''',
                 r'''Геометрический закон:

$E(X) = \frac{1}{p}$

$Var(X) = \frac{q}{p^2}$

<hr>

Свойства:

$E(X) = E(E(X|Y))$

$Var(X) = E(Var(X|Y)) + Var(E(X|Y))$

<hr>

Для заданий:

Пусть $S$ - сумма очков, $X$ - монета, $N$ - количество орлов

Вероятность ровно k орлов:

$P(N=k) = C_n^k \cdot p^k \cdot p^{n - k}$, где $p=\frac{1}{2}$ - вероятность выпадения орла, $n$ - всего монет

$E(N) = \frac{1}{P(N=k)}$

$Var(N) = \frac{1 - P(N=k)}{P^2(N=k)}$

* $E(S|N) = E(X_1 + X_2 + ... + X_N | N) = E(X_1) + ... + E(X_N) = E(X) \cdot N \Rightarrow \color{orange}{E(S)} = E(E(S|N)) = E(N\cdot E(X)) = \color{orange}{E(N) \cdot E(X)}$

<br>

* $E(Var(S|N)) = E(Var(X_1) + ... + Var(X_N)) = E(N\cdot Var(X)) = Var(X) \cdot E(N)$

<br>

* $Var(E(S|N)) = Var(E(X)\cdot N) = E^2(X)\cdot Var(N)$

<br>

* $\color{orange}{std(S) = \sqrt{Var(S)} = \sqrt{E(Var(S|N)) + Var(E(S|N))}}$
```

q = 29
k = 8

p_1 = 1/2
p_k = math.comb(q, k) * 1/2**k * 1/2**(q-k)
times = 1 / p_k #геом распр
times_var = (1 - p_k)/(p_k)**2

e_dice = 3.5
var_dice = 35/12

#геом закон - сколько раз бросится кубик, чтобы выпало 8 орлов, так получаем количетсво - times
#в среднем на кубике выпадает e_dice, а его кинули times раз
ans1 = e_dice * times

E_Var__S_N = times * var_dice
Var_E__S_N = times_var * e_dice**2

ans2 = np.sqrt(E_Var__S_N + Var_E__S_N)

answer(ans1, ans2)
```'''),
            8:
                (r'''В группе учится 29 студентов. Ими были получены следующие 100-балльные оценки: 90, 79, 53, 62, 66, 68, 75, 0, 82, 29, 0, 29, 68, 90, 0, 60, 44, 44, 70, 68, 70, 89, 0, 68, 0, 66, 0, 59, 70. Найдите: 1) A – среднюю положительную оценку в группе; 2) M – медиану положительных оценок в группе; 3) H – среднее гармоническое и G – среднее геометрическое оценок, которые не менее M; 4) Q – медианную оценку в той части группы, в которой студенты набрали не менее M баллов; 5) N – количество студентов, оценки которых оказались между H и Q (включая границы).''',
                 r'''Пусть $Arr = np.array(...)$, тогда:

* $Arr[Arr > 0]$, $Arr[Arr <>= k]$ - маски, позволяющие отбирать положительные значения или значения, $<>=$ данного числа $k$

* $A = Arr.mean()$, где $.mean()$ - среднее

* $M = np.median(Arr)$, где $np.median()$ - метод для выявления медианы в массиве

* $H = hmean(Arr)$ - метод ($scipy.stats$) для выявления среднего гармонического ($\frac{n}{\sum_{i=1}^{n}{\frac{1}{x_i}}}$)

* $G = gmean(Arr)$ - метод ($scipy.stats$) для выявления среднего геометрического ($\sqrt{x_1 \cdot x_2 \cdot ... \cdot x_n}$)
```

grades = [90, 79, 53, 62, 66, 68, 75, 0, 82, 29, 0, 29, 68, 90, 0, 60, 44, 44, 70, 68, 70, 89, 0, 68, 0, 66, 0, 59, 70]

grades = np.array(grades)
n = len(grades)

A = grades[grades > 0].mean()
M = np.median(grades[grades > 0])
H = hmean(grades[grades >= M])
G = gmean(grades[grades >= M])
Q = np.median(grades[grades >= M])
N = len(grades[(grades >= Q) & (grades <= H)])

answer(A, M, H, G, Q, N)
```'''),
            9:
                (r'''Следующие 28 чисел – это умноженные на 10000 и округленные до ближайшего целого дневные логарифмические доходности акции компании АВС: -9, 9, -138, -145, 186, 78, 34, -37, -19, -68, -82, 158, 96, -189, 24, 84, -99, 125, -39, 26, 62, -91, 239, -211, 2, 129, 2, -16. Будем называть их преобразованными доходностями (ПД). Финансовый аналитик Глеб предполагает, что преобразованные доходности (как и исходные) приближенно распределены по нормальному закону. Чтобы проверить свое предположение Глеб нашел нижнюю квартиль L и верхнюю квартиль H нормального распределения $N(μ,σ^2)$
, для которого μ
 – это среднее арифметическое ПД, а σ
 – эмпирическое стандартное отклонение ПД. Затем Глеб подсчитал количество ПД, попавших в интервал от L до H (надеясь, что в этот интервал попадет половина ПД). Результат этого вычисления показался ему недостаточно убедительным. Чтобы окончательно развеять сомнения относительно нормальности ПД, Глеб построил на одном рисунке графики функций: $\hat F(x)$ и F(x), где $\hat F(x)$ – эмпирическая функция распределения ПД, а F(x) – функция распределения $N(μ,σ^2)$. В качестве меры совпадения двух графиков Глеб решил использовать расстояние d между функциями $\hat F(x)$ и F(x), которое он вычислил, исходя из определения: $d=sup|\hat F(x)−F(x)|$. В ответе укажите результаты вычислений Глеба: 1) среднее арифметическое ПД; 2) эмпирическое стандартное отклонение ПД; 3) квартили L и H; 4) количество ПД, попавших в интервал от L до H; 5) расстояние между функциями $\hat F(x)$ и F(x).''',
                 r'''Пусть $Arr = np.array(...)$, тогда:

* $Arr[Arr > 0]$, $Arr[Arr <>= k]$ - маски, позволяющие отбирать положительные значения или значения, $<>=$ данного числа $k$

* $Arr.mean()$ - среднее арифметическое

* $Arr.std()$ - эмпирическое стандартное отклонение

Имея среднее и std, можем задать нормальный закон:

$X = norm(E, std)$

* $L = X.ppf(0.25)$ - нижняя квартиль

* $H = X.ppf(0.75)$ - верхяя квартиль

* $H = hmean(Arr)$ - метод ($scipy.stats$) для выявления среднего гармонического ($\frac{n}{\sum_{i=1}^{n}{\frac{1}{x_i}}}$)

* $G = gmean(Arr)$ - метод ($scipy.stats$) для выявления среднего геометрического ($\sqrt{x_1 \cdot x_2 \cdot ... \cdot x_n}$)

* $d = |\frac{i + 1}{n} - X.cdf(sorted(Arr)[i]|$ - функция расстояния для i-го отстортированного по взорастанию элемента $Arr$
```

pd = [-9, 9, -138, -145, 186, 78, 34, -37, -19, -68, -82, 158, 96, -189, 24, 84, -99, 125, -39, 26, 62, -91, 239, -211, 2, 129, 2, -16]

pd = np.array(pd)
n = len(pd)

E = pd.mean()

std = pd.std()

X = norm(E, std)

L = X.ppf(0.25)
H = X.ppf(0.75)

N = len(pd[(pd > L) & (pd < H)])

mx = -10**100
pdsort = sorted(pd)

for i in range(n):
    temp = abs((i + 1) / n - X.cdf(pdsort[i]))
    mx = max(mx, temp)

answer(E, std, L, H, N, mx)
```'''),
            10:
                (r'''В группе Ω учатся студенты: $ω_1,...,ω_30$. Пусть X и Y – 100-балльные экзаменационные оценки по математическому анализу и теории вероятностей. Оценки студента $ω_i$ обозначаются: $x_i=X(ω_i)$ и $y_i=Y(ω_i)$, i=1,...,30. Все оценки известны: x1=71,y1=71
, x2=52,y2=58
, x3=72,y3=81
, x4=87,y4=92
, x5=81,y5=81
, x6=100,y6=94
, x7=90,y7=96
, x8=54,y8=46
, x9=54,y9=60
, x10=58,y10=62
, x11=56,y11=49
, x12=70,y12=60
, x13=93,y13=86
, x14=46,y14=48
, x15=56,y15=61
, x16=59,y16=52
, x17=42,y17=40
, x18=60,y18=60
, x19=33,y19=37
, x20=83,y20=92
, x21=50,y21=57
, x22=93,y22=93
, x23=41,y23=42
, x24=55,y24=64
, x25=60,y25=59
, x26=37,y26=30
, x27=71,y27=71
, x28=42,y28=44
, x29=85,y29=82
, x30=39,y30=39
. Требуется найти следующие условные эмпирические характеристики: 1) ковариацию X и Y при условии, что одновременно X⩾50 и Y⩾50; 2) коэффициент корреляции X и Y при том же условии.''',
                 r'''$Cov(X, Y) = E(XY) - E(X) \cdot E(Y)$ или $np.cov(X, Y, ddof=0)[0, 1]$

$\rho = \frac{Cov(X, Y)}{\sigma_X\cdot \sigma_Y}$ или $np.corrcoef(X, Y)[0, 1]$
```

data = x1=71,y1=71
 , x2=52,y2=58
, x3=72,y3=81
, x4=87,y4=92
, x5=81,y5=81
, x6=100,y6=94
, x7=90,y7=96
, x8=54,y8=46
, x9=54,y9=60
, x10=58,y10=62
, x11=56,y11=49
, x12=70,y12=60
, x13=93,y13=86
, x14=46,y14=48
, x15=56,y15=61
, x16=59,y16=52
, x17=42,y17=40
, x18=60,y18=60
, x19=33,y19=37
, x20=83,y20=92
, x21=50,y21=57
, x22=93,y22=93
, x23=41,y23=42
, x24=55,y24=64
, x25=60,y25=59
, x26=37,y26=30
, x27=71,y27=71
, x28=42,y28=44
, x29=85,y29=82
, x30=39,y30=39

x = []
y = []

for line in data.split('\n'):
    temp = line.split('=')
    y.append(int(temp[-1]))
    x.append(int(temp[1].split(',')[0]))

x, y = np.array(x), np.array(y)

x_and_y = np.concatenate([x.reshape(-1, 1), y.reshape(-1, 1)], axis = 1)
result = x_and_y[(x_and_y[:, 0] >= 50) & (x_and_y[:, 1] >= 50)]
cov = np.prod(result, axis=1).mean() - result[:, 0].mean() * result[:, 1].mean()
ro = cov / (result[:, 0].std() * result[:, 1].std())
cov, ro

x50 = []
y50 = []

for i in range(len(x)):
    if x[i] >= 50 and y[i] >= 50:
        x50.append(x[i])
        y50.append(y[i])

x50, y50 = np.array(x50), np.array(y50)

cov = (x50 * y50).mean() - x50.mean() * y50.mean()

ro = cov / (x50.std() * y50.std())

answer(cov, ro)

answer(np.cov(x50, y50, ddof=0)[0, 1], np.corrcoef(x50, y50)[0, 1])
```'''),
            11:
                (r'''Поток Ω состоит из k групп: $Ω_1,...,Ω_k$, k=3. На потоке учатся $n=n_1+...+n_k$ студентов, где $n_i$ – число студентов в группе $Ω_i$, i=1,...,k. Пусть X(ω) – 100-балльная оценка студента $ω∈Ω$. Далее используются следующие обозначения: $\overline x_i$ – среднее значение, $σ_i$ – (эмпирическое) стандартное отклонение признака X на группе $Ω_i$. Дано: n1=24
, n2=26
, n3=30
, x¯¯¯1=70
, x¯¯¯2=76
, x¯¯¯3=77
, σ1=4
, σ2=6
, σ3=8
. Требуется найти: 1) среднее значение X
 на потоке Ω
; 2) (эмпирическое) стандартное отклонение X
 на потоке Ω
.''',
                 r'''* $E = \frac{\sum{n_i \cdot x_i}}{\sum{n_i}}$

* $\sigma^2 = \frac{\sum{n_i \cdot (x_i - E)^2}}{\sum{n_i}}$

* $s^2 = \frac{\sum{n_i \cdot \sigma_i^2}}{\sum{n_i}}$

* $std = \sqrt{Var} = \sqrt{\sigma^2 + s^2}$
```

k = 3
n = np.array([24, 26, 30])
x = np.array([70, 76, 77])
s = np.array([4, 6, 8])

E = sum(n * x) / sum(n)

Var_all = sum(n * (x - E) ** 2) / sum(n)
Var_E_all = sum(n * s ** 2) / sum(n)
Var = Var_all + Var_E_all
std = np.sqrt(Var)

answer(E, std)
```'''),
            12:
                (r'''В группе Ω
 учатся 27
 студентов, Ω={1,2,...,27}
. Пусть X(i)
 – 100-балльная оценка студента $i∈Ω$
. Из группы Ω
 случайным образом 7
 раз выбирается студент $ω∈Ω$
. Повторный выбор допускается. Пусть $ω_j$
 – студент, полученный после выбора j=1,...,7
, $X(ω_j)$
 – его оценка. Среднюю оценку на случайной выборке обозначим $\overline X=\frac {1}{7}\sum X(ω_j)$
. Оценки в группе даны: 100, 86, 51, 100, 95, 100, 12, 61, 0, 0, 12, 86, 0, 52, 62, 76, 91, 91, 62, 91, 65, 91, 9, 83, 67, 58, 56. Требуется найти: 1) дисперсию $Var(\overline X)$
; 2) центральный момент $μ_3(\overline X)$
.''',
                 r'''
```
grades = [100, 86, 51, 100, 95, 100, 12, 61, 0, 0, 12, 86, 0, 52, 62, 76, 91, 91, 62, 91, 65, 91, 9, 83, 67, 58, 56]
k = 7

grades = np.array(grades)
n = len(grades)

var = grades.var() / k

mu3 = moment(grades, 3) / k ** 2
# или:
# mu3 = np.sum((grades - grades.mean()) ** 3) / n / k ** 2

answer(var, mu3)
```'''),
            13:
                (r'''В группе Ω
 учатся 27
 студентов, Ω={1,2,...,27}
. Пусть X(i)
 – 100-балльная оценка студента i∈Ω
. Из группы Ω
 случайным образом 6
 раз выбирается студент $ω∈Ω$
. Повторный выбор не допускается. Пусть $ω_j$
 – студент, полученный после выбора j=1,...,6
, $X(ω_j)$
 – его оценка. Среднюю оценку на случайной выборке обозначим $\overline X=\frac{1}{6}\sum X(ω_j)$
. Оценки в группе даны: 100, 78, 77, 51, 82, 100, 73, 53, 78, 55, 7, 0, 81, 15, 96, 12, 71, 70, 53, 0, 73, 100, 55, 100, 59, 89, 81. Требуется найти: 1) математическое ожидание $E(\overline X)$
; 2) дисперсию $Var(\overline X)$
.''',
                 r'''
```
grades = [100, 78, 77, 51, 82, 100, 73, 53, 78, 55, 7, 0, 81, 15, 96, 12, 71, 70, 53, 0, 73, 100, 55, 100, 59, 89, 81]
k = 6

grades = np.array(grades)
n = len(grades)

E = grades.mean()

Var = grades.var() / k * (n - k) / (n - 1)

answer(E, Var)
```'''),
            14:
                (r'''Распределение баллов на экзамене до перепроверки задано таблицей
Оценка работыЧисло работ

$\begin{array}{|c|c|}
\hline
оценка работы&2&3&4&5\\
\hline
число работ&76&48&8&105\\
\hline
\end{array}$.

Работы будут перепроверять 6 преподавателей, которые разделили все работы между собой поровну случайным образом. Пусть $\overline X$
 – средний балл (до перепроверки) работ, попавших к одному из преподавателей. Требуется найти: 1) математическое ожидание $E(\overline X)
$; 2) стандартное отклонение $σ(\overline X)$''',
                 r'''
```
vals = [2] * 7 + [3] * 48 + [4] * 8 + [5] * 105
k = 6

vals = np.array(vals)
n = len(vals)
k = n / k

E = vals.mean()

Var = vals.var() / k * (n - k) / (n - 1)
std = np.sqrt(Var)

answer(E, std)
```'''),
            15:
                (r'''Две игральные кости, красная и синяя, подбрасываются до тех пор, пока не выпадет 19 различных (с учетом цвета) комбинаций очков. Пусть $R_i$
 – число очков на красной кости, а $B_i$
 – число очков на синей кости в комбинации с номером i
. Случайные величины $X_i$
 задаются соотношениями: $X_i=11R_i−9B_i,i=1,...,19$
. Среднее арифметическое этих величин обозначим $\overline X=\frac{1}{19}\sum X_i$
. Требуется найти: 1) математическое ожидание $E(\overline X)$
; 2) стандартное отклонение $σ(\overline X)$
.''',
                 r'''
```
k = 19
n = 36

combs = [(r, b) for r in range(1, 7) for b in range(1, 7)]
combs = np.array(combs)
mean, var = combs.mean(axis=0), combs.var(axis=0)

E = 11 * mean[0] - 9 * mean[1]

Var = 121 * var[0] + 81 * var[1]
Var = Var / k * (n - k) / (n - 1)
std = np.sqrt(Var)

answer(E, std)
```'''),
            16:
                (r'''Имеется 11 пронумерованных монет. Монеты подбрасываются до тех пор, пока не выпадет 257 различных (с учетом номера монеты) комбинаций орел-решка. Пусть $X_i$
 – число орлов в комбинации с номером i
; а $\overline X=\frac {1}{257}\sum X_i$
 – среднее число орлов в полученных таким образом комбинациях. Требуется найти: 1) математическое ожидание $E(\overline X)$
; 2) дисперсию $Var(\overline X)$
.''',
                 r'''
```
k = 257
q = 11

n = 2 ** q

lst = np.array(list(itertools.product([0, 1], repeat=q)))

E = lst.mean() * q

Var = lst.var() * q
Var = Var / k * (n - k) / (n - 1)

answer(E, Var)
```'''),
            17:
                (r'''Эмпирическое распределение признаков X
 и Y
 на генеральной совокупности Ω={1,2,...,100}
 задано таблицей частот

$\begin{array}{|c|c|}
\hline
&Y=1&Y=2&Y=3\\
\hline
X=100&11&32&11\\
\hline
X=400&24&11&11\\
\hline
\end{array}$

Из Ω
 случайным образом без возвращения извлекаются 7 элементов. Пусть $\overline  X$
 и $\overline Y$
 – средние значения признаков на выбранных элементах. Требуется найти: 1) математическое ожидание $E(\overline X)$
; 2) дисперсию $Var(\overline Y)$
; 3) коэффициент корреляции $ρ(\overline X,\overline Y)$
.''',
                 r'''
```
vals = [(100, 1)] * 11 + [(100, 2)] * 32 + [(100, 3)] * 11 + \
[(400, 1)] * 24 + [(400, 2)] * 11 + [(400, 3)] * 11
k = 7

vals = np.array(vals)
n = len(vals)

E = vals.mean(axis=0)[0]

VarY = vals.var(axis=0)[1]
VarY = VarY / k * (n - k) / (n - 1)

cov = np.cov(vals[:, 0], vals[:, 1], ddof=0)[0, 1] / k * (n - k) / (n - 1)

VarX = vals.var(axis=0)[0]
VarX = VarX / k * (n - k) / (n - 1)

ro = cov / (np.sqrt(VarX) * np.sqrt(VarY))

# проще (без cov и VarX):
# ro = np.corrcoef(vals[:, 0], vals[:, 1])

answer(E, VarY, ro)
```'''),
            18:
                (r'''Эмпирическое распределение признаков X
 и Y
 на генеральной совокупности Ω={1,2,...,100}
 задано таблицей частот

$\begin{array}{|c|c|}
\hline
&Y=1&Y=2&Y=4\\
\hline
X=100&21&17&12\\
\hline
X=300&10&27&13\\
\hline
\end{array}$

Из Ω
 случайным образом без возвращения извлекаются 6 элементов. Пусть $\overline  X$
 и $\overline Y$
 – средние значения признаков на выбранных элементах. Требуется найти: 1) математическое ожидание $E(\overline Y)$
; 2) стандартное отклонение $σ(\overline X)$
; 3) ковариацию $Cov(\overline X,\overline Y)$
.''',
                 r'''
```
vals = [(100, 1)] * 21 + [(100, 2)] * 17 + [(100, 4)] * 12 + \
[(300, 1)] * 10 + [(300, 2)] * 27 + [(300, 4)] * 13
k = 6

vals = np.array(vals)
n = len(vals)

E = vals.mean(axis=0)[1]

VarX = vals.var(axis=0)[0]
VarX = VarX / k * (n - k) / (n - 1)
stdX = np.sqrt(VarX)

cov = np.cov(vals[:, 0], vals[:, 1], ddof=0)[0, 1] / k * (n - k) / (n - 1)

answer(E, stdX, cov)
```'''),
            19:
                (r'''Глеб и Анна исследуют эффективность лекарственного препарата АВС. Глеб, используя модель Анны, создал компьютерную программу, вычисляющую по заданным генетическим факторам вероятность (в процентах) успешного применения АВС. Программа Глеба накапливает полученные вероятности и в итоге выдает набор частот: $n_0,n_1,...,n_100$
. Например, $n_75$
 – это число случаев, в которых программа Глеба получила вероятность 75%. Обработав 1000 образцов генетического материала, Анна нашла значения факторов и ввела их в программу. В результате был получен следующий набор частот: 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 3, 4, 4, 5, 4, 6, 6, 11, 9, 19, 23, 25, 33, 36, 36, 46, 46, 49, 58, 90, 76, 66, 69, 75, 68, 44, 39, 21, 16, 5, 2, 1, 0, 0, 0. Для завершения этапа исследования необходимо было подобрать распределение, соответствующее полученным частотам. Анна решила использовать распределение на отрезке [0,1]
 с плотностью $f(x)=f(x;a,b)=abx^{a−1}(1−x^a)^{b−1}$
 и целочисленными параметрами a,b
 в диапазоне от 1 до 20. В результате максимизации функции правдоподобия (при указанных ограничениях) Глебом были получены значения параметров: $\hat a=A$
 и $\hat b=B$
. Задача: пусть X
 – случайная величина, распределения на отрезке [0,1]
 с плотностью $f(x)=f(x;\hat a,\hat b)$
, F(x)
 – ее функция распределения. Требуется найти математическое ожидание E(X)
 и $X_{0, 2}=F^{−1}(0,2)$
 – квантиль уровня 0,2. Какой смысл для всей популяции имеют E(X)
 и $X_{0, 2}$
? В ответе укажите: 1) значение A
; 2) значение B
; 3) математическое ожидание E(X)
; 4) квантиль $X_{0, 2}$
.''',
                 r'''По условию дан массив частот - необходимо его преобразовать в массив-выборку.
Например, если напротив числа "90" в частотном массиве стоит "8", то это означает, что в выборке число "90" появилось 8 раз (порядок не имеет значения).

Рассчитаем функцию правдоподобия:

$L(a, b) = f(x_1, a, b) \cdot f(x_2, a, b) \cdot ... \cdot f(x_n, a, b)$

$L(a, b) = abx_1^{a-1}(1-x_1^a)^{b-1} \cdot ... \cdot abx_n^{a-1}(1-x_n^a)^{b-1}$

$L(a, b) = a^nb^n(x_1x_2...x_n)^{a-1}((1-x_1^a)(1-x_2^a)...(1-x_n^a))^{b-1}$

$l = ln(L) = \color{orange}{n\cdot ln(ab) + (a-1)\cdot\sum{ln(x_i)} + (b-1)\cdot\sum{ln(1 - x_i^a)}}$

Для нахождения параметров $a$ и $b$ достаточно перебрать все комбинации чисел в промежутке $[1; 20]$ и найти такую, при котором функция $l = ln(L)$ будет иметь максимальное значение.

Для нахождения математического ожидания необходимо рассчитать интеграл:

$\color{orange}{E(X) = \int_0^1{x\cdot f(x)dx}}$

Для нахождения квантиля необходимо задать распределение с данным $pdf$ и воспользоваться перебором в цикле или запомнить следующую формулу (квантильная функция):

$\color{orange}{F^{-1}(q, a, b) = (1 - (1 - q) ^ \frac{1}{b}) ^ \frac{1}{a}}$
```

q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0,
     1, 1, 3, 4, 4, 5, 4, 6, 6, 11, 9, 19, 23, 25, 33, 36, 36, 46, 46, 49, 58, 90, 76, 66, 69, 75, 68,
     44, 39, 21, 16, 5, 2, 1, 0, 0, 0]
quantil = 0.2

# преобразование в массив-выборку

sample = []
for i in range(len(q)):
    temp = [i] * q[i]
    sample.extend(temp)
sample = np.array(sample) / 100

# функция из задания

def f(x, a, b):
    return a * b * x ** (a - 1) * (1 - x ** a) ** (b - 1)

# рассчитанная функция правдоподобия

def lnL(p, data):
    n = len(data)
    a, b = p
    return n * np.log(a * b) + (a - 1) * np.sum(np.log(data)) + (b - 1) * np.sum(np.log(1 - data ** a))

# поиск наилучших оценок a и b

mx, mx_a, mx_b = 0, 0, 0

for a in range(1, 21):
    for b in range(1, 21):
        prod = lnL([a, b], sample)
        if prod > mx:
            mx = prod
            mx_a = a
            mx_b = b

# расчёт мат ожидания (from scipy import integrate)

E = integrate.quad(lambda x: x * f(x, mx_a, mx_b), 0, 1)[0]

# задаём свой класс распределения

class distr(rv_continuous):
    def _pdf(self, x):
        if 0 <= x <= 1:
            return a * b * x ** (a - 1) * (1 - x ** a) ** (b - 1)
        return 0

X = distr()

# высчитываем квантиль

current_quantil = 0

prec = 15
p = 0

d = 1

while p < prec:
    if X.cdf(current_quantil) <= quantil:
        current_quantil += d
    else:
        current_quantil -= d
        d /= 10
        p += 1

# или:
# current_quantil = (1 - (1 - quantil) ** (1 / mx_b)) ** (1 / mx_a)

answer(mx_a, mx_b, E, current_quantil)

```
## решение через библиотеку
```

q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0,
     1, 1, 3, 4, 4, 5, 4, 6, 6, 11, 9, 19, 23, 25, 33, 36, 36, 46, 46, 49, 58, 90, 76, 66, 69, 75, 68,
     44, 39, 21, 16, 5, 2, 1, 0, 0, 0]
quantil = 0.2

# преобразование в массив-выборку

sample = []
for i in range(len(q)):
    temp = [i] * q[i]
    sample.extend(temp)
sample = np.array(sample) / 100

# рассчитанная функция правдоподобия
def logL(data, a, b):
    return len(data)*np.log(a*b) + (a-1) * np.sum(np.log(data)) + (b-1) * np.sum(np.log(1 - data**a))

# поиск наилучших оценок a и b

ma = 0

for a in range(1, 21):
    for b in range(1, 21):
        logL_temp = logL(sample, a, b)
        if ma < logL_temp:
            ma = logL_temp
            res_a = a
            res_b = b


from kumaraswamy import kumaraswamy
K = kumaraswamy(res_a, res_b)

# расчёт мат ожидания (from scipy import integrate)

E = K.mean

current_quantil = K.ppf(quantil)

answer(mx_a, mx_b, E, current_quantil)
```'''),
            20:
                (r'''Пусть $(x_1,y_1);...;(x_{31},y_{31})$
 – реализация случайной выборки $(X1_,Y_1);...;(X_{31},Y_{31})$
 из двумерного нормального распределения $N(μ_x;μ_y;σ^2_x;σ^2_y;ρ)$
. Используя векторы $\overrightarrow x =(x_1;...;x_{31})$
 и $\overrightarrow y =(y_1;...;y_{31})$
, постройте асимптотический 0,93-
доверительный интервал $(\hat θ_1;\hat θ_2)$
 для коэффициента корреляции ρ
. В ответе укажите: 1) выборочный коэффициент корреляции $hat ρ$;
 2) верхнюю границу $\hat θ_2$
 построенного доверительного интервала для ρ
.
Исходные данные: x
 = (-0,616; -0,238; 0,173; -0,255; 0,531; 0,718; -0,161; 0,371; -1,014; -0,413; -1,571; 0,485; 0,486; 0,688; -0,944; 0,155; 0,003; 0,111; 0,752; 0,783; -0,102; -0,74; -2,097; 1,349; -0,044; -0,617; -0,782; -0,873; -0,995; -1,256; -0,596),   y
 = (-1,34; -0,25; 0,101; -0,626; -0,088; 0,539; -0,451; 0,233; -1,186; -0,423; -1,329; 0,231; 0,209; 0,638; -0,274; -0,491; -0,319; 0,294; 0,895; 1,164; -0,57; -1,078; -1,526; 1,491; 0,182; -0,31; -1,001; -0,969; -0,918; -0,904; -0,595).''',
                 r'''Формула для выборочного коэффициента корреляции $\hat\rho$:

$\hat\rho = \frac{\widehat{Cov}(x, y)}{\hat\sigma_x \hat\sigma_y}$

В питоне выборочную ковариацию можно посчитать с помощью:

$np.cov(x, y, \color{orange}{ddof=0})[0, 1]$ (возвращает ковариационную матрицу, где элемент [0, 1] или [1, 0] является ковариацией)

В питоне выборочное стандартное отклонение считается как:

$\Large x.std()$

Формулы для границ выборочного коэффициента корреляции:

$\hat{u}_{1,n} = arth(\hat\rho) - \frac{1}{\sqrt{n-3}}\cdot z_\frac{\alpha}{2}$

$\hat{u}_{2,n} = arth(\hat\rho) + \frac{1}{\sqrt{n-3}}\cdot z_\frac{\alpha}{2}$

$arth(x)$ - ареатангенс, в питоне эквивалент: $np.arctanh(x)$

Однако в данном случае мы получим оценку для параметра $arth(\hat\rho)$

Чтобы получить оценку для коэффициента корреляции, нам необходимо взять обратную функцию для полученных промежутков:
* Обратная функция $arth(x)$ $\Large -$ $tanh(x)$
* Тогда интервал составит $(tanh(\hat{u}_{1,n}),  tanh(\hat{u}_{2,n}))$
* В питоне для просчёта обратной функции используется $np.tanh(x)$
```

x = np.array([-0.616, -0.238, 0.173, -0.255, 0.531, 0.718, -0.161, 0.371, -1.014, -0.413, -1.571, 0.485,
              0.486, 0.688, -0.944, 0.155, 0.003, 0.111, 0.752, 0.783, -0.102, -0.74, -2.097, 1.349, -0.044,
              -0.617, -0.782, -0.873, -0.995, -1.256, -0.596])
y = np.array([-1.34, -0.25, 0.101, -0.626, -0.088, 0.539, -0.451, 0.233, -1.186, -0.423, -1.329, 0.231,
              0.209, 0.638, -0.274, -0.491, -0.319, 0.294, 0.895, 1.164, -0.57, -1.078, -1.526, 1.491, 0.182,
              -0.31, -1.001, -0.969, -0.918, -0.904, -0.595])
gamma = 0.93

n = len(x)

Z = norm(0, 1)

ro_hat = np.cov(x, y, ddof=0)[0, 1] / x.std() / y.std()
ro_hat

u_left = np.arctanh(ro_hat) - 1 / np.sqrt(n - 3) * Z.isf((1 - gamma) / 2)
u_right = np.arctanh(ro_hat) + 1 / np.sqrt(n - 3) * Z.isf((1 - gamma) / 2)

left = np.tanh(u_left)
right = np.tanh(u_right)

answer(left, right, ro_hat)
```'''),
            21:
                (r'''Пусть $\overrightarrow x =(x_1,…,x_{30})$
 – реализация случайной выборки $\overrightarrow X =(X_1,…,X_{30})$
 из нормального распределения $N(μ;{3,4}^2)$
. Проверяется на уровне значимости α=0,01
 основная гипотеза H0:μ=1,29
 против альтернативной гипотезы H1:μ≠1,29
 с критическим множеством вида $K_α=(−∞,−A)∪(A,+∞)$
. 1) Найдите значение статистики критерия $Z_{набл.}=Z(\overrightarrow x )$
. 2) Найдите границу А критического множества. 3) Найдите P
-значение критерия и сделайте выводы. 4) Найдите мощность W
 критерия для H1:μ=1,17
.
Исходные данные: x =
 (1,416; 0,624; 6,471; 6,256; 1,787; 2,546; -1,758; -5,475; 0,077; 1,792; 5,443; 5,348; -0,057; 0,232; -2,305; -3,568; -4,541; 7,893; -0,473; -0,229; -3,0; 3,903; -4,227; 0,537; -1,785; 2,575; -0,477; -2,754; 1,164; 2,716).''',
                 r'''Ищем $ \mu$, известна $\sigma$:

$Z = \frac{(\overline{x} - \mu)\sqrt{n}}{\sigma}$ - статистика

$A = Z_\frac{\alpha}{2}$

$\beta = \Phi_0(A - \frac{(\mu_1 - \mu_0)\sqrt{n}}{\sigma}) + \Phi_0(A + \frac{(\mu_1 - \mu_0)\sqrt{n}}{\sigma})$

*tip: структура $\frac{(\overline{x} - \mu)\sqrt{n}}{\sigma}$ встречается в нескольких местах (в т.ч. и дальше), если это знать, то её так проще запомнить*
```

x = convert('1,416; 0,624; 6,471; 6,256; 1,787; 2,546; -1,758; -5,475; 0,077; 1,792; 5,443; 5,348; -0,057; 0,232; -2,305; -3,568; -4,541; 7,893; -0,473; -0,229; -3,0; 3,903; -4,227; 0,537; -1,785; 2,575; -0,477; -2,754; 1,164; 2,716')
x = np.array(x)
n = len(x)

s = 3.4
alpha = 0.01
mu0 = 1.29
mu1 = 1.17

z = np.sqrt(n) * (x.mean() - mu0) / s

A = Z.isf(alpha / 2)

P = 2 * min(Z.cdf(z), Z.sf(z))

beta = Phi0(A - np.sqrt(n) * (mu1 - mu0) / s) + Phi0(A + np.sqrt(n) * (mu1 - mu0) / s)
W = 1 - beta

answer(z, A, P, W)
```'''),
            22:
                (r'''Пусть $x =(x_1,…,x_{20})$
 – реализация случайной выборки $X =(X_1,…,X_{20})$
 из нормального распределения $N(μ;σ^2)$
. Проверяется на уровне значимости α=0,05
 основная гипотеза $H_0:μ=1,10$
 против альтернативной гипотезы $H_1:μ≠1,10$
 с критическим множеством вида $K_α=(−∞,−A)∪(A,+∞)$
. 1) Найдите значение статистики критерия $t=T_{набл.}=T(x)$
. 2) Найдите границу А критического множества. 3) Найдите P
-значение критерия и сделайте выводы. 4) Найдите мощность W
 критерия для H1:μ=0,91
.
Исходные данные: x =
 (1,146; 2,958; -3,325; -0,534; 0,374; 5,293; 0,12; 1,185; 5,148; 5,351; 2,639; 1,47; -1,967; 4,96; 6,057; -0,542; 1,544; -0,243; -1,988; 2,844).''',
                 r'''Ищем $\mu$, неизвестна $\sigma$:

$T = \frac{(\overline{x} - \mu)\sqrt{n - 1}}{s}$, где s - исправленное выборочное отклонение (ddof=0, стоит по умолчанию)

$A = t_\frac{\alpha}{2}(n-1)$

$\beta = G_{n-1, \delta}(A) - G_{n-1, \delta}(-A)$,

где $\delta = \frac{\sqrt{n - 1}(\mu_1 - \mu_0)}{s}$, где s - исправленное выборочное отклонение (ddof=0, стоит по умолчанию)

*tip: если то, что мы НЕ ищем, неизвестно, то это связано с (n - 1) вместо (n) (дальше также будет); структура из 1-ого пункта повторяется; ddof=0 необязательно прописывать, оно по умолчанию*
```

x = convert('1,146; 2,958; -3,325; -0,534; 0,374; 5,293; 0,12; 1,185; 5,148; 5,351; 2,639; 1,47; -1,967; 4,96; 6,057; -0,542; 1,544; -0,243; -1,988; 2,844')
x = np.array(x)
n = len(x)

alpha = 0.05
mu0 = 1.1
mu1 = 0.91

T = np.sqrt(n - 1) * (x.mean() - mu0) / x.std(ddof=0)

A = t(n - 1).isf(alpha / 2)

P = 2 * min(t(n - 1).cdf(T), t(n - 1).sf(T))

delta = np.sqrt(n - 1) * (mu1 - mu0) / x.std()

beta = nct(n - 1, delta).cdf(A) - nct(n - 1, delta).cdf(-A)
W = 1 - beta

answer(T, A, P, W)
```'''),
            23:
                (r'''Пусть $x =(x_1,…,x_{30})$
 – реализация случайной выборки $X =(X_1,…,X_{30})$
 из нормального распределения $N(1,18;σ^2)$
. Проверяется на уровне значимости α=0,02
 гипотеза $H_0:σ=1,14$
 против альтернативной гипотезы $H_1:σ≠1,14$
 с критическим множеством вида $K_α=(0;A)∪(B;+∞)$
. 1) Найдите значение статистики критерия $χ^2_0$
. 2) Найдите границы А и В критического множества и проверьте гипотезу H0
. 3) Найдите P
-значение критерия. 4) Найдите вероятность ошибки второго рода β
 для $σ_1=1,24$
. Исходные данные: x =
 (0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821).''',
                 r'''Ищем $\sigma$, известна $\mu$:

$\chi = \frac{ns^2}{s_0^2}$, где $s^2 = \frac{\sum{(x_i - \mu)^2}}{n}$ - дисперсия с известным $\mu$

$A = \chi^2_{1 - \frac{\alpha}{2}}(n)$

$B = \chi^2_{\frac{\alpha}{2}}(n)$

$\beta = \chi^2(n).cdf(\frac{s_0^2}{s_1^2}\cdot B) - \chi^2(n).cdf(\frac{s_0^2}{s_1^2}\cdot A) $

*tip: быть внимательным при подсчёте A и B - в левой границе используется (1 -), в правой нет; не перепутать местами B и A при подсчёте beta - проще запомнить формулу так: из больше (B) вычитаем меньшее (A)*
```

x = convert('0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821')
x = np.array(x)
n = len(x)

alpha = 0.02
mu = 1.18
s0 = 1.14
s1 = 1.24

s2 = np.sum((x - mu) ** 2) / n
CHI = n * s2 / s0 ** 2

A = chi2(n).isf(1 - alpha / 2)
B = chi2(n).isf(alpha / 2)

P = 2 * min(chi2(n).cdf(CHI), chi2(n).sf(CHI))

beta = chi2(n).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n).cdf(s0 ** 2 / s1 ** 2 * A)

answer(CHI, A, B, P, beta)
```'''),
            24:
                (r'''Пусть $x =(x_1,…,x_{30})$
 – реализация случайной выборки $X =(X_1,…,X_{30})$
 из нормального распределения $N(μ;σ^2)$
. Проверяется на уровне значимости α=0,02
 гипотеза $H_0:σ=1,14$
 против альтернативной гипотезы $H_1:σ≠1,14$
 с критическим множеством вида $K_α=(0;A)∪(B;+∞)$
. 1) Найдите значение статистики критерия $χ^2$
. 2) Найдите границы А и В критического множества и проверьте гипотезу H0
. 3) Найдите P
-значение критерия. 4) Найдите вероятность ошибки второго рода β
 для $σ_1=1,24$
. Исходные данные: x =
 (0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821).''',
                 r'''Ищем $\sigma$, неизвестна $\mu$:

$\chi = \frac{ns^2}{s_0^2}$, где $s^2$ - исправленная выборочная дисперсия (ddof=0, стоит по умолчанию)

$A = \chi^2_{1 - \frac{\alpha}{2}}(n - 1)$

$B = \chi^2_{\frac{\alpha}{2}}(n - 1)$

$\beta = \chi^2(n - 1).cdf(\frac{s_0^2}{s_1^2}\cdot B) - \chi^2(n - 1).cdf(\frac{s_0^2}{s_1^2}\cdot A) $

*tip: всё точно так же, как в предыдущей задаче, только вместо true дисперсии берём выборочную, степень свободы (n) заменяем на (n - 1)*
```

x = convert('0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821')
x = np.array(x)
n = len(x)

alpha = 0.02
s0 = 1.14
s1 = 1.24

CHI = n * x.var() / s0 ** 2

A = chi2(n - 1).isf(1 - alpha / 2)
B = chi2(n - 1).isf(alpha / 2)

P = 2 * min(chi2(n - 1).cdf(CHI), chi2(n - 1).sf(CHI))

beta = chi2(n - 1).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n - 1).cdf(s0 ** 2 / s1 ** 2 * A)

answer(CHI, A, B, P, beta)
```'''),
            25:
                (r'''Пусть $x =(x_1,…,x_{25})$
 – реализация случайной выборки $X =(X_1,…,X_{25})$
 из нормального распределения $N(μ_x;0,7^2)$
, а $y =(y_1,…,y_{30})$
 – реализация случайной выборки Y$ =(Y_1,…,Y_30)$
 из нормального распределения $N(μ_y;1,4^2)$
. Известно, что X
 и Y
 независимы. Проверяется гипотеза $H_0:μ_x=μ_y$
 против альтернативной гипотезы $H_1:μ_x>μ_y$
. При уровне значимости α
 применяется критерий с критической областью {Z>A}
, где статистика критерия $Z=Z(X ,Y)$
 – это нормированная разность $\overline X−\overline Y$
, $A=A_α$
 – зависящее от α
 критическое значение. Соответствующее критическое множество имеет вид $K_α=(A_α;∞)$
. 1) Найдите значение статистики критерия $Z_{набл.}=Z(x ,y)$
. 2) Найдите P
-значение критерия. 3) Найдите критическое значение A
, критическое множество $K_α$
 и проверьте гипотезу $H_0$
 при α=0,02
. 4) Найдите мощность критерия W
 в случае $μ_x−μ_y=0,1$
 и α=0,02
. Исходные данные: x =
 (3,842; 3,374; 4,18; 4,5; 4,247; 4,412; 3,756; 3,946; 3,729; 3,948; 3,631; 2,992; 4,324; 3,919; 3,059; 4,524; 3,565; 4,236; 4,71; 4,29; 4,998; 3,336; 4,482; 3,721; 3,59); y =
 (3,19; 3,564; 4,079; 2,369; 5,261; 4,652; 1,849; 6,084; 6,654; 5,65; 3,748; 2,501; 5,476; 3,436; 5,711; 4,292; 5,367; 4,499; 4,989; 4,015; 6,5; 4,178; 4,563; 6,636; 2,113; 2,221; 5,357; 2,358; 6,721; 3,421).''',
                 r'''Проверяем $\mu_x = \mu_y$:

$Z = \frac{\overline{X} - \overline{Y}}{\sqrt{\frac{\sigma_X^2}{n} + \frac{\sigma_Y^2}{m}}}$

$A = Z_\alpha$

$\beta = \frac{1}{2} + \Phi_0(A - \frac{\sqrt{nm}}{\sqrt{m\sigma_X^2 + n\sigma_Y^2}} \cdot \Delta) = Z.cdf(A - \frac{\sqrt{nm}}{\sqrt{m\sigma_X^2 + n\sigma_Y^2}} \cdot \Delta)$

*tip: формулы сложные, придётся запомнить - не забыть главное, что в формуле беты в знаменателе особое умножение!!! не $(len(x) \cdot \sigma_x^2 + len(y) \cdot \sigma_y^2)$, а НАОБОРОТ, $(len(x) \cdot \sigma_y^2 + len(y) \cdot \sigma_x^2)$*
```

x = convert('3,842; 3,374; 4,18; 4,5; 4,247; 4,412; 3,756; 3,946; 3,729; 3,948; 3,631; 2,992; 4,324; 3,919; 3,059; 4,524; 3,565; 4,236; 4,71; 4,29; 4,998; 3,336; 4,482; 3,721; 3,59')
x = np.array(x)
n = len(x)

y = convert('3,19; 3,564; 4,079; 2,369; 5,261; 4,652; 1,849; 6,084; 6,654; 5,65; 3,748; 2,501; 5,476; 3,436; 5,711; 4,292; 5,367; 4,499; 4,989; 4,015; 6,5; 4,178; 4,563; 6,636; 2,113; 2,221; 5,357; 2,358; 6,721; 3,421')
y = np.array(y)
m = len(y)

sx = 0.7
sy = 1.4
alpha = 0.02
delta = 0.1

z = (x.mean() - y.mean()) / np.sqrt(sx ** 2 / n + sy ** 2 / m)

P = Z.sf(z)

A = Z.isf(alpha)

beta = Z.cdf(A - np.sqrt(m * n) / np.sqrt(m * sx ** 2 + n * sy ** 2) * delta)
W = 1 - beta

answer(z, P, A, W)
```'''),
            26:
                (r'''Для трех групп финансовых показателей $A: (X_1;...;X_{27})
, B: (Y_1;...;Y_{33})
, C: (Z_1;...;Z_{39})$
, которые по предположению независимы и распределены, соответственно, по трем нормальным законам $N(μ_x,σ^2)
, N(μ_y,σ^2)
, N(μ_z,σ^2)$
 (с одинаковой неизвестной дисперсией $σ^2$
) на уровне значимости α=0,01
 с помощью F-критерия (Фишера) проверяется гипотеза $H0:μ_x=μ_y=μ_z$
 о совпадении ожидаемых значений показателей. Конкретные значения всех показателей указаны ниже. 1) По данным значениям показателей найдите межгрупповую дисперсию. 2) По этим же данным найдите среднюю групповую дисперсию. 3) Найдите значение статистики F-критерия, критическое множество $K_α$
 и проверьте гипотезу H0
. 4) Найдите P
-значение критерия и сделайте выводы.
Значения показателей группы A: (0,616; 1,046; 2,575; -0,344; 2,339; -0,68; 3,739; 2,251; -1,252; 3,536; -0,491; 5,556; 4,856; -1,68; 2,33; 1,345; 2,829; 2,539; 3,304; 3,497; 0,211; 3,563; 0,94; 3,642; 1,956; 3,919; 3,568). Значения показателей группы B: (2,834; 1,504; -0,678; 5,619; 0,97; 1,617; 3,768; -1,309; 3,343; -1,778; -0,854; 1,04; 2,83; -2,335; 4,853; 5,6; 4,341; 4,362; 3,52; 1,151; -0,621; -2,88; 1,697; 1,753; 0,211; 2,157; 1,989; 2,457; 1,399; 1,61; -0,558; 2,132; 2,293). Значения показателей группы C: (2,398; -2,77; 4,679; 1,924; 0,574; 5,329; 0,699; 4,457; -0,3; 1,682; -1,34; 0,046; -1,096; 1,935; 2,411; 4,134; 5,643; 3,071; 6,526; 4,941; 2,844; -0,43; -2,066; 0,22; 0,317; -1,923; 1,38; -2,485; 0,111; -0,542; 4,78; 1,93; 0,462; 5,487; -3,547; 2,933; -0,987; -0,21; 3,955).''',
                 r'''Проверяем $\mu_x = \mu_y = \mu_z$:

$\delta^2 = \frac{1}{n}\sum_{i=1}^{k}{(\overline{X_i} - \overline{X}) ^ 2 n_i}$ — межгрупповая дисперсия

$\overline{\sigma^2} = \frac{1}{n}\sum_{i=1}^{k}{\hat{\sigma}^2_i n_i}$ — средняя групповая дисперсия

$A = f(k - 1, N - k)_\alpha$

$\mathbb F = \frac{MSTR}{MSE} = \frac{(n - k)\delta^2}{(k - 1)\overline{\sigma^2}}$, где

<hr>

$MSE = \frac{SSE}{n - k}$ — остаточная дисперсия

$SSE = n \cdot \overline{\sigma^2}$ — внутригрупповая сумма квадратов

<hr>

$MSTR = \frac{SSTR}{k - 1}$ — факторная дисперсия

$SSTR = n \cdot \delta^2$ — межгрупповая сумма квадратов

*tip: ну тут только бог поможет. мне кажется проще запомнить сразу формулу для F через дельта и среднюю сигму, чем запоминать все 4 квадратичных отклонения, в которых можно запутаться. при подсчёте везде ddof=0 по умолчанию*

Если гипотеза о равенстве средних в группах отвергается, то имеет смысл найти доверительный интервал для каждой оценки.

$\Large \mathbb P(\hat{\theta}_{1i} < \mu_i < \hat{\theta}_{2i}) = \gamma = 1 - \alpha$

$\Large \hat\theta_{1i} = \overline X_i - t_\frac{\alpha}{2}(n - k)\cdot\sqrt{\frac{MSE}{n_i}}$

$\Large \hat\theta_{2i} = \overline X_i + t_\frac{\alpha}{2}(n - k)\cdot\sqrt{\frac{MSE}{n_i}}$

```

x = convert('0,616; 1,046; 2,575; -0,344; 2,339; -0,68; 3,739; 2,251; -1,252; 3,536; -0,491; 5,556; 4,856; -1,68; 2,33; 1,345; 2,829; 2,539; 3,304; 3,497; 0,211; 3,563; 0,94; 3,642; 1,956; 3,919; 3,568')
x = np.array(x)
n1 = len(x)

y = convert('2,834; 1,504; -0,678; 5,619; 0,97; 1,617; 3,768; -1,309; 3,343; -1,778; -0,854; 1,04; 2,83; -2,335; 4,853; 5,6; 4,341; 4,362; 3,52; 1,151; -0,621; -2,88; 1,697; 1,753; 0,211; 2,157; 1,989; 2,457; 1,399; 1,61; -0,558; 2,132; 2,293')
y = np.array(y)
n2 = len(y)

z = convert('2,398; -2,77; 4,679; 1,924; 0,574; 5,329; 0,699; 4,457; -0,3; 1,682; -1,34; 0,046; -1,096; 1,935; 2,411; 4,134; 5,643; 3,071; 6,526; 4,941; 2,844; -0,43; -2,066; 0,22; 0,317; -1,923; 1,38; -2,485; 0,111; -0,542; 4,78; 1,93; 0,462; 5,487; -3,547; 2,933; -0,987; -0,21; 3,955')
z = np.array(z)
n3 = len(z)

xyz = pd.DataFrame([x, y, z]).T
xyz_all = np.concatenate([x, y, z])
n = [n1, n2, n3]
N = sum(n)
k = 3

alpha = 0.01

d2 = np.sum((xyz.mean() - xyz_all.mean()) ** 2 * n) / N

meanvar = np.sum(xyz.var(ddof=0) * n) / N

F = (N - k) * d2 / (k - 1) / meanvar

A = scs.f(k - 1, N - k).isf(alpha)

P = scs.f(k - 1, N - k).sf(F)

answer(d2, meanvar, F, P)

# для считывания из файла

#data = pd.read_csv('sample.csv', header=None, decimal=',', sep=';', encoding='cp1251')
#x, y, z = data[0], data[1], data[2]
#x = x.dropna()
#y = y.dropna()
#z = z.dropna()

#доверительные интервалы
left = xyz.mean() - t(N - k).isf((1 - 0.9) / 2) * np.sqrt(MSE / n)
right = xyz.mean() + t(N - k).isf((1 - 0.9) / 2) * np.sqrt(MSE / n)

for mu, l, r in zip(xyz.mean(), left, right):
    print(f"{l:.6f} < {mu:.6f} < {r:.6f}")
```'''),
            27:
                (r'''По содержащейся в файле ds.6.4.1.csv реализации случайной выборки из двумерного нормального распределения $N((E(X); E(Y)); \begin{Vmatrix}
Var(X) & Cov(X, Y)\\
Cov(X, Y) & Var(Y)
\end{Vmatrix}) = ((-3; 2); \begin{Vmatrix}
\sigma^2 & \rho\sigma^2\\
\rho\sigma^2 & \sigma^2
\end{Vmatrix})$ с неизвестными параметрами $\rho \in (-1; 1)$ и $\sigma > 0$ запишите логарифм функции правдоподобия, lnL($\rho \sigma$); 2) найдите оценки максимального правдоподобия $\hat{\rho}$ и $\hat{\sigma}$.''',
                 r'''
```
data_x = -0,448726722
-4,077760635
-3,502739215
-1,66318003
-4,644781096
-4,068438401
-6,448639082
-1,515451889
-1,345900844
-3,836516493
-2,832250421
-3,107639238
-2,678514264
-2,414763469
-3,41182319
-2,702918302
-1,286748914
-2,238655269
-2,18659518
-2,368898426
-3,892325758
-1,305921773
-2,652178311
-1,998093358
-2,840195104
-4,453586548
-1,632042627
-2,844678731.replace(',', '.').split()

data_y = -1,508540881
2,519984715
3,726214206
3,004836083
0,277423308
3,632152644
1,754934396
1,206677064
2,652454826
1,95208093
0,720844353
3,731719773
3,147530165
2,643239983
2,023704916
2,071973179
2,910559417
2,459073356
3,086424729
-1,486183114
1,847036332
1,555575181
2,694073633
0,950173357
2,3873016
3,38970961
2,874189768
3,420221845
.replace(',', '.').split()

data_x = np.array(list(map(float, data_x)))
data_y = np.array(list(map(float, data_y)))

mx = -3
my = 2
```
$\Large f(x_1, x_2) = \frac{1}{2\pi\sigma_1\sigma_2\sqrt{1 - \rho^2}}e^{-\frac{1}{2(1-\rho^2)}\left(\frac{(x_1 - \mu_1)^2}{\sigma_1^2} - 2\rho\frac{(x_1 - \mu_1)(x_2 - \mu_2)}{\sigma_1\sigma_2} + \frac{(x_2 - \mu_2)^2}{\sigma_2^2}\right)}$

$\Large L = \frac{1}{(2\pi\sigma_1\sigma_2\sqrt{1 - \rho^2})^n}e^{-\frac{1}{2(1-\rho^2)\sigma^2}\sum{((x+3)^2_i - 2\rho(x+3)_i(y-2)_i + (y-2)^2_i)}}$

$l = ln(L) = n \cdot ln(\frac{1}{2\pi\sigma_1\sigma_2\sqrt{1 - \rho^2}}) -\frac{1}{2(1-\rho^2)\sigma^2}\sum{((x+3)^2_i - 2\rho(x+3)_i(y-2)_i + (y-2)^2_i)}$

<br>

Пусть $A = \overline{(x + 3)^2} \Rightarrow \sum{(x+3)^2_i} = nA$,

$B = \overline{(y - 2)^2} \Rightarrow \sum{(y-2)^2_i} = nB$,

$C = \overline{(x + 3)(y - 2)} \Rightarrow \sum{(x+3)_i(y-2)_i} = nC$

<br>

Тогда:

$\color{orange}{ln(L) = -nln(2pi) - nln(\sigma^2) - \frac{n}{2}ln(1-\rho^2) -\frac{n}{2(1-\rho^2)\sigma^2}(A - 2\rho C + B)}$

Пусть $\sigma^2 = x, \rho = y$
```
sigma, ro, y, A, B, C, x, y, n = sp.symbols('sigma rho y A B C x y n')

lnL = -n * sp.log(2 * sp.pi) - n * sp.log(x) - n / 2 * sp.log(1 - y ** 2) - n / (2 * x * (1 - y ** 2)) * (A + B - 2 * y * C)
lnL

dx = sp.Derivative(lnL, x, evaluate=True)
dx

dy = sp.Derivative(lnL, y, evaluate=True)
dy

res = sp.solve([dx, dy], [x, y])[0]

res[0].simplify()

res[1].simplify()

A_ = np.mean((data_x + 3) ** 2)
B_ = np.mean((data_y - 2) ** 2)
C_ = np.mean((data_x + 3) * (data_y - 2))

s_hat = np.sqrt(0.5 * (A_ + B_))
r_hat = 2 * C_ / (A_ + B_)
s_hat, r_hat
```'''),
        }
    }
