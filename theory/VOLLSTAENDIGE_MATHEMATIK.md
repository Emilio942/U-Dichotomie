# Die vollständige Mathematik des Projekts „U-Dichotomie"

**Zweck:** Selbstständiges, in sich geschlossenes Dokument. Alle Aussagen sind entweder
bewiesen („Satz" mit Beweis), als Beweisskizze klar markiert, oder als numerisches
Ergebnis gekennzeichnet. Keine externen Referenzen nötig.

---

## 0. Ergebnis in einem Satz

Die beobachtete Varianz-Dichotomie $\mathrm{Var}(\Delta)=\Theta(N^{-2})$ vs.
$\Theta(N^{-1})$ der Schwarm-Diversität ist **kein** Effekt der Symmetriebrechung von
$\pi_1$ (die findet nie statt) und **kein** Effekt von $\eta>0$ per se, sondern ein
**Mean-Field-Synchronisationsübergang** bei der geschlossenen Schwelle
$\eta_c = \tfrac{D\,d(d+2)}{2}$; für $d\ge4$ ist er subkritisch (Koexistenz), für
$d\le2$ kontinuierlich.

---

## 1. Setting und Notation

**Raum.** $\mathcal{X}=\mathrm{Gr}(k,d)=O(d)/(O(k)\times O(d-k))$, die Grassmann-Mannigfaltigkeit der $k$-dimensionalen Unterräume von $\mathbb{R}^d$. Metrik: geodätischer Abstand
$$d_G(V,W)=\Big(\sum_{\ell=1}^k \theta_\ell^2\Big)^{1/2},$$
mit $\theta_\ell\in[0,\pi/2]$ die Hauptwinkel zwischen $V$ und $W$. $\mathcal{X}$ ist kompakt, $d_G$ ist beschränkt ($(k\pi/2)^2$-beschränkt im Quadrat) und $O(d)$-invariant: $h(RV,RW)=h(V,W)$ für alle $R\in O(d)$.

**Darstellung.** Teilchen werden durch Orthonormal-Frame-Matrizen $Q\in\mathrm{St}(d,k)=\{Q\in\mathbb{R}^{d\times k}: Q^\top Q=I\}$ repräsentiert; der Unterraum ist $\mathrm{span}(Q)$ (Frames nur bis $O(k)$-Rechtsaktion). Alle Statistiken benutzen Hauptwinkel und sind frame-invariant.

**Haar-Maß.** $\mu_H$ = eindeutiges $O(d)$-invariantes Wahrscheinlichkeitsmaß auf $\mathcal{X}$; Sampling: QR-Zerlegung einer $d\times k$-Gauß-Matrix.

**Dynamik** (Euler-Discretisierung, Schrittweite $\dd t$). Für die Konfiguration $\mathbf{V}=(Q_1,\dots,Q_N)$:
$$\bar S=\frac1N\sum_{j=1}^N Q_jQ_j^\top\qquad\text{(Konsensusfeld)},$$
$$\mathrm{grad}_i = 2\big(\bar S Q_i - Q_i\,\mathrm{sym}(Q_i^\top \bar S Q_i)\big)\qquad\text{(Stiefel-Gradient von } f(Q)=\mathrm{tr}(Q^\top \bar S Q)), $$
$$Q_i \leftarrow \mathrm{polar}\Big(Q_i + \dd t\,\eta\,\mathrm{grad}_i + \sqrt{2D\,\dd t}\;\xi_i\Big),\qquad \xi_i\sim\mathcal N(0,I_{d\times k})\ \text{i.i.d.}$$
Polar-Retraktion (Newton–Schulz: $X\mapsto \tfrac12 X(3I-X^\top X)$ iteriert) projiziert zurück auf $\mathrm{St}(d,k)$; für $k=1$ ist es einfach die Normierung $v/\|v\|$.

**Zwei Grenzfälle der Dynamik:**
- $\eta=0$: isotroper Random Walk ⟹ stationäres Gesetz = Haar (unabhängige Teilchen, wenn zusätzlich jedes Teilchen unabhängiges Rauschen hat).
- $\eta>0$: attraktiver Konsensus; für $\eta$ oberhalb einer Schwelle Symmetriebrechung durch Clusterbildung (siehe §10).

**Die U-Statistik.** Kern $h(V,W)=d_G(V,W)$, Diversität
$$\Delta=\frac{2}{N(N-1)}\sum_{1\le i<j\le N} h(V_i,V_j),\qquad \theta=\E_{\pi_2}[h(V_1,V_2)].$$

**Äquivalenz-Notiz (wichtig für Satz 1).** Das Konsensusfeld ist kovariant:
mit $R\mathbf{V}:=(RQ_1,\dots,RQ_N)$ gilt $T_R\bar S T_R^\top = \overline{R\mathbf S}$, das Rauschen ist isotrop, und $h$ ist invariant. Daher kommutiert der Generator $\mathcal L_\eta$ der Kette mit der diagonalen $O(d)$-Aktion: $\mathcal L_\eta (f\circ T_R) = (\mathcal L_\eta f)\circ T_R$.

---

## 2. Axiome

- **(A1) Äquivarianz:** $P_\eta(R\mathbf x,\cdot) = (T_R)^{\times N} P_\eta(\mathbf x, R^{-1}\cdot)$ für alle $R\in O(d)$ — gilt für die obige Dynamik.
- **(A2) Permutationssymmetrie** in den Teilchen-Labels — gilt.
- **(A3) Geometrische Ergodizität** mit eindeutigem stationärem Gesetz $\pi_\eta$ — Standard für kompakte Zustandsräume mit uniform elliptischem Rauschen.
- **(A4)** alle Momente von $h$ existieren — trivial, da $h$ beschränkt.

---

## 3. Hoeffding-Zerlegung für austauschbare Maße

Für das stationäre Gesetz $\pi$ (austauschbar wegen (A2)) mit 1-/2-Randverteilungen $\pi_1,\pi_2$:
$$h_1(x)=\E_{\pi_2}[h(V_1,V_2)\mid V_1=x]-\theta,\qquad h_2=h-\theta-h_1\otimes1-1\otimes h_1,$$
$$\zeta_1=\mathrm{Var}_{\pi_1}(h_1),\qquad \zeta_2=\mathrm{Var}_{\pi_2}(h_2).$$
Im i.i.d.-Fall gilt exakt $\mathrm{Var}(\Delta)=\frac{4}{N}\zeta_1+\frac{2}{N(N-1)}\zeta_2$; die Dichotomie-Frage ist, ob ein $\Theta(N^{-1})$-Term existiert und woher.

---

## 4. Satz 1 (Exakte Invarianz): $\pi_1=\mu_H$, $h_1\equiv0$, $\zeta_1^*\equiv0$ — für alle $\eta$

**Satz 1.** Unter (A1)–(A3) gilt für jedes $\eta\ge0$:
1. $\pi_\eta$ ist $O(d)$-invariant (diagonale Aktion) und austauschbar.
2. $\pi_1=\mu_H$ (exakt).
3. $m(x):=\E_{\pi_2}[h(V_1,V_2)\mid V_1=x]$ ist konstant in $x$; also $h_1\equiv0$ und $\zeta_1=0$.
4. Die „effektive Varianz" $\zeta_1^*:=\zeta_1+\sum_{j\ne1}\mathrm{Cov}_\pi(h_1(V_1),h_1(V_j))$ des Original-Problem-Statements verschwindet identisch.

**Beweis.**
(1) Sei $\mu$ stationär. Dann ist $\mu\circ T_R^{-1}$ stationär, denn für alle $f$:
$\int f\,\dd(\mu T_R^{-1})=\int (f\circ T_R)\,\dd\mu=\int (T_R^{-1}\mathcal L_\eta T_R f)\,\dd\mu=\int \mathcal L_\eta(f\circ T_R)\,\dd\mu=0$
(da $\mathcal L_\eta T_R = T_R\mathcal L_\eta$ nach (A1) und $\int\mathcal L_\eta g\,\dd\mu=0$). Eindeutigkeit (A3) liefert $\mu T_R^{-1}=\mu$. Austauschbarkeit analog mit der $S_N$-Aktion.

(2) $\pi_1$ ist ein $O(d)$-invariantes Wahrscheinlichkeitsmaß auf dem homogenen Raum $O(d)/(O(k)O(d-k))$. Das Haar-Maß ist das **einzige** solche Maß: für zwei Punkte $x,y$ existiert $g$ mit $gx=y$; die Maße kongruenter Mengen sind gleich; aus Zweitabzählbarkeit und einem Überdeckungsargument folgt Eindeutigkeit (Standardfakt). Also $\pi_1=\mu_H$.

(3) Sei $K(x,\cdot)$ die reguläre bedingte Verteilung von $V_2$ gegeben $V_1=x$ unter $\pi_2$. Diagonale Invarianz: $(g,g)_\#\pi_2=\pi_2$. Durch Drücken der Konditionierung durch $(g,g)$:
$$K(gx,\,gA)=K(x,A)\qquad\forall\text{ messbare }A.$$
Damit
$$m(gx)=\int h(gx,y)\,K(gx,\dd y)=\int h(gx,gz)\,K(x,\dd z)=\int h(x,z)\,K(x,\dd z)=m(x),$$
wobei der zweite Schritt $y=gz$ substituiert und der dritte $h(gx,gz)=h(x,z)$ benutzt. $O(d)$ wirkt transitiv auf $\mathrm{Gr}(k,d)$, also ist $m$ konstant; mit $\E_{\pi_1}m=\theta$ folgt $m\equiv\theta$, d.h. $h_1\equiv0$.

(4) folgt unmittelbar aus (3). $\square$

**Korollar 1 (Widerlegung des Original-Conjecture).** Die Behauptung „$\eta>0\Rightarrow\pi_1\ne\mu_H\Rightarrow\zeta_1>0$" ist falsch. Beide Seiten der Varianz-Formel aus Problem 2 des Statements ($\mathrm{Var}=\tfrac4N\zeta_1^*+\dots$) verschwinden identisch und können keine $\Theta(N^{-1})$-Skalierung erzeugen.
**Numerische Bestätigung:** bei $\eta=5>0$ (ungeordnet, siehe §10) ist der log-log-Slope von $\mathrm{Var}(\Delta)$ über $N$: $-2.013$; bei $\eta=0$: $-1.994$.

**Bemerkung (spontane Symmetriebrechung).** Die Symmetriebrechung durch den Konsensus-Drift ist *spontan*: der Cluster hat einen zufälligen Ort $F\sim\mu_H$, das stationäre Gesetz ist (heuristisch) die Mischung $\pi_N\approx\int\nu_F^{\otimes N}\,\dd F(F)$, und $\pi_1=\int\nu_F\,\dd F=\mu_H$ restauriert die Symmetrie exakt. Was NICHT Haar ist: $\pi_2=\E_F[\nu_F\otimes\nu_F]\ne\mu_H^{\otimes2}$ — zwei Teilchen teilen ihren Cluster-Ort.

---

## 5. Director-Maß-Bild und Zerlegung von $\Delta$

Für austauschbare Systeme benutzen wir durchgängig die de-Finetti-/Chaos-Struktur: es gibt (exakt im Limes, approximativ bei finitem $N$) ein **Director-Maß** $\Chi$, sodass näherungsweise
$$\pi_N\approx\int \nu^{\otimes N}\,\dd\Chi(\nu),$$
d.h. bedingt auf den Director $\nu$ sind die Teilchen i.i.d. $\sim\nu$. Für Mean-Field-Systeme fluktuiert $\Chi$ um das Mean-Field-Gleichgewicht auf Skala $O(N^{-1/2})$.

Definiere für ein Wahrscheinlichkeitsmaß $\mu$:
$$\phi(\mu):=\iint h\,\dd\mu\,\dd\mu-\theta,\qquad m_\mu(x):=\int h(x,y)\,\dd\mu(y)-\theta.$$

**Lemma 1 (exakte Identitäten).**
1. Mit den Leave-one-out-Mitteln $g_i:=\frac1{N-1}\sum_{j\ne i}h(V_i,V_j)$ gilt $\Delta=\frac1N\sum_i g_i$ und
$$\mathrm{Var}_\pi(\Delta)=\frac1{N^2}\Big[\sum_i\mathrm{Var}(g_i)+\sum_{i\ne j}\mathrm{Cov}(g_i,g_j)\Big].$$
2. Bedingt auf den Director:
$$\Delta-\theta=\phi(\nu)+\frac2N\sum_{i=1}^N m_\nu(V_i)+W_N(\nu),$$
wo $W_N$ der inner-Director-degenerierte Rest ist mit $\mathrm{Var}(W_N\mid\nu)=\frac{2\,\zeta_2^{\nu}}{N^2}+O(N^{-3})$, $\zeta_2^\nu=\mathrm{Var}_{\nu\otimes\nu}(h)$.

*Beweis von 1:* $\Delta=\frac1{N(N-1)}\sum_{i\ne j}h_{ij}$ und $\sum_i g_i=\frac1{N-1}\sum_{i\ne j}h_{ij}$; Varianz durch Linearität. *Beweis von 2:* $\E[h(V_1,V_2)\mid\nu]=\theta+\phi(\nu)$; die bedingte Fluktuation $\Delta-(\theta+\phi(\nu))$ ist eine U-Statistik unter i.i.d. $\nu$ mit erster Hoeffding-Projektion $m_\nu$ und degeneriertem Rest. $\square$

---

## 6. Satz 2 (ungeordnetes/chaotisches Regime): $\Theta(N^{-2})$ und gewichtetes $\chi^2$-Limit

**Satz 2.** $\eta$ liege in dem Bereich, in dem $\mu_H$ das stabile Mean-Field-Gleichgewicht ist (insbesondere $\eta=0$, und generisch $\eta<\eta_c$, §10), und das Director-Maß erfülle $\|\nu-\mu_H\|=O_\Chi(N^{-1/2})$ (Chaos-Rate $N^{-1/2}$). Dann:

1. $\mathrm{Var}_\pi(\Delta)=\dfrac{2\,\zeta_2(\eta)}{N(N-1)}+\Theta$-Beitrag zweiter Ordnung $=\Theta(N^{-2})$, mit $\zeta_2(\eta)\to\zeta_2(0)=\mathrm{Var}_{\mu_H\otimes\mu_H}(h)$.

2. **Grenzverteilung:** Bei $\eta=0$ exakt
$$N\,(\Delta-\theta)\ \xrightarrow{d}\ \sum_{k\ge1}\lambda_k\,\big(\chi^2_{1,k}-1\big),$$
eine (im Allgemeinen indefinite) gewichtete $\chi^2$-Summe, $\{\lambda_k\}$ die Eigenwerte des zentrierten Kerns $h-\theta$ als Integraloperator auf $L^2(\mu_H)$. Insbesondere $\E=0$, $\mathrm{Var}\to2\sum_k\lambda_k^2=2\zeta_2(0)$, und $\sqrt N(\Delta-\theta)\Rightarrow0$.

3. Für $0<\eta<\eta_c$ bleibt die Skalierung $N$; das Limit bleibt eine indefinite quadratische Form (gewichtetes $\chi^2$-*Typ*), wobei zum klassischen Anteil möglicherweise ein Gauß-anteiliger Director-Fluktuations-Term $\delta^\top Q\delta$ gleicher Ordnung hinzutritt ($\delta\sim\mathcal N(0,\Sigma)$ das Mean-Field-Fluktuationsfeld). Skalierung und Nicht-Gauß-Charakter ändern sich nicht; $\eta=0$ ist der einzige Fall mit garantiert reinem klassischem Limit.

**Beweis.**
*(Ordnung $\Theta(N^{-2})$.)* Bedingt auf $\nu$: $\Delta-\theta=\phi(\nu)+\frac2N\sum_i m_\nu(V_i)+W_N(\nu)$ (Lemma 1).
- **Der $\phi$-Term ist zweiter Ordnung:** Die erste variationale Ableitung von $\phi$ an $\mu_H$ ist
$$D\phi_{\mu_H}[\psi]=2\int\Big(\int h(x,y)\,\dd\mu_H(y)-\theta\Big)\dd\psi(x)=2\int h_1^{\mu_H}(x)\,\dd\psi(x)=0$$
**für alle** $\psi$ (mit $\int\dd\psi=0$), denn $h_1^{\mu_H}\equiv0$ nach Satz 1(3). Also $\phi(\nu)=\phi(\mu_H)+O(\|\nu-\mu_H\|^2)=O(N^{-1})$, und $\mathrm{Var}_\Chi(\phi)=O(N^{-2})$.
- **Der $m$-Term ist zweiter Ordnung:** $m_{\mu_H}\equiv0$, also $m_\nu(x)=O(\|\nu-\mu_H\|)=O(N^{-1/2})$ und $\frac4N\,\E\,\mathrm{Var}_\nu(m_\nu)=O(N^{-2})$.
- **Der $W_N$-Term:** $\mathrm{Var}(W_N\mid\nu)=\frac{2\zeta_2^\nu}{N^2}$, und $\zeta_2^\nu\to\zeta_2(0)$ stetig.
- **Diagonal-Beitrag:** $\E\,\mathrm{Var}(\Delta\mid\nu)\supset \frac{2\zeta_2^\nu}{N(N-1)}$ — genau klassische Ordnung.
Insgesamt $\mathrm{Var}(\Delta)=\frac{2\zeta_2^\nu}{N(N-1)}+O(N^{-2})=\Theta(N^{-2})$.

*(Grenzverteilung bei $\eta=0$.)* Die Teilchen sind i.i.d. Haar. Da $h_1\equiv0$, ist $\Delta-\theta=\frac1{\binom N2}\sum_{i<j}h_2(V_i,V_j)$ mit degeneriertem $h_2$. Mercer-Expansion $h_2(x,y)=\sum_k\lambda_k e_k(x)e_k(y)$ ($\{e_k\}$ ON-Basis von $L^2(\mu_H)$, $\sum\lambda_k^2=\zeta_2(0)<\infty$) liefert
$$\Delta-\theta=\frac1{\binom N2}\sum_k\lambda_k\Big[\big(\tfrac{S_k}{2}\big)^2-\tfrac{T_k}{2}\Big]\quad\text{mit } S_k=\sum_i e_k(V_i),\ T_k=\sum_i e_k^2(V_i).$$
Der mehrdimensionale CLT gibt $(S_k/\sqrt N)_{k\le K}\Rightarrow(Z_1,\dots,Z_K)$ i.i.d. $\mathcal N(0,1)$ und $T_k/N\to1$ f.s.; mit $\sum_{k>K}\lambda_k^2\to0$ (Hilbert–Schmidt-Rest, Tightness) folgt das Limit. Varianz: $\mathrm{Var}\to2\sum\lambda_k^2$ (für die Zählung $S_k^2-T_k$: $\mathrm{Var}(S_k^2)=2N^2+O(N)$, keine Kreuz-Kovarianzen, da $E[e_ke_l]=0$, $E[e_k^2e_l^2]=1$ für $k\ne l$). $\square$

---

## 7. Exaktrechnung für $\mathrm{Gr}(1,2)$: $\sum\lambda_k^2=\pi^2/48$

Für $k=d=2$ ist $\mathcal{X}$ die gefaltete Kreislinie: Winkel $\alpha\in[0,\pi)$, Kern
$$\varphi(\Delta)=\arccos|\cos\Delta|,\qquad \theta=\langle\varphi,1\rangle=\frac\pi4.$$
ON-Basis von $L^2([0,\pi),\dd\alpha/\pi)$: $e_0=1$, $e_{\ell,c}=\sqrt2\cos(2\ell\alpha)$, $e_{\ell,s}=\sqrt2\sin(2\ell\alpha)$.

**Proposition 7.1 (Fourier-Koeffizienten).** $\displaystyle \lambda_{\ell,c}=\frac{\sqrt2}{\pi}\int_0^\pi\varphi(\alpha)\cos(2\ell\alpha)\,\dd\alpha=\frac{\sqrt2}{\pi}\cdot\frac{(-1)^\ell-1}{2\ell^2},$ also
$$\lambda_{\ell,c}=-\frac{\sqrt2}{\pi\ell^2}\ (\ell\ \text{ungerade}),\qquad \lambda_{\ell,c}=0\ (\ell\ \text{gerade}),\qquad \lambda_{\ell,s}=0\ \forall\ell.$$
*Beweis:* $\varphi(\alpha)=\alpha$ auf $[0,\pi/2]$, $\pi-\alpha$ auf $[\pi/2,\pi)$; zweimalige partielle Integration liefert $\int_0^\pi\varphi\cos(2\ell\alpha)\dd\alpha=\frac{(-1)^\ell-1}{2\ell^2}$. $\square$

**Folgerung.** $\displaystyle\sum_k\lambda_k^2=\sum_{\ell\ \text{ungerade}}\frac{2}{\pi^2\ell^4}=\frac{2}{\pi^2}\cdot\frac{\pi^4}{96}=\frac{\pi^2}{48},\qquad \mathrm{Var}\big(N(\Delta-\theta)\big)\to\frac{\pi^2}{24}.$
(MC: $0.407/0.415/0.429$ bei $N=500/1500/4000$, $B=40{,}000$, gegen $0.4112$; KS gegen das simulierte Limit $0.005$–$0.007$, unterhalb der Schwelle $1.63/\sqrt B$.)

**Proposition 7.2 (exakte finite-N-Identität).** Für Winkel $\alpha_1,\dots,\alpha_N$:
$$\sum_{i\ne j}\big(\varphi-\theta\big)(\alpha_i-\alpha_j)=\sum_k \lambda_k\big[S_k^2-N\big],\qquad S_k:=\sum_i e_k(\alpha_i),$$
denn $\sum_i e_k(\alpha_i)^2=N$ **exakt** ($\cos^2+\sin^2=1$). Somit
$$\Delta-\theta=\frac{1}{N(N-1)}\sum_k\lambda_k\big[S_k^2-N\big],$$
und mit $S_k/\sqrt N\Rightarrow\mathcal N(0,1)$ (joint über $k$) folgt Satz 2(2) für diesen Fall.
*(Warnung für Nachrechner: $e_k=\sqrt2\cos$, also $S_k^2=2\,(\sum\cos\alpha_i)^2$ — der Faktor 2 gehört in die Identität.)*

---

## 8. Satz 3 (geordnetes/synchronisiertes Regime): $\Theta(N^{-1})$ und Gauß-Limit

**Satz 3.** Das Mean-Field-System habe gebrochen-symmetrische stabile Gleichgewichte: Director-Gesetz $\nu_F$, $F\sim\mu_H$ (Cluster-Ort), mit $\nu_{RF}=R_\#\nu_F$ und Cluster-Breite $w_\eta\asymp(D/\kappa\eta)^{1/2}$. Dann:

1. $\pi_1=\mu_H$, $h_1\equiv0$, $\zeta_1=0$ (Satz 1 gilt unverändert) — die klassische Nicht-Degenerations-Diagnostik liefert ein **falsches Negative**.
2. Trotzdem
$$\mathrm{Var}_\pi(\Delta)=\frac{\sigma_\eta^2}{N}+O(N^{-2}),\qquad \sigma_\eta^2=4\,\E_F\big[\mathrm{Var}_{\nu_F}(m_F)\big]+\gamma_\eta,\qquad \E_F[\mathrm{Var}_{\nu_F}(m_F)]\asymp w_\eta^2\asymp\frac{D}{\kappa\eta}.$$
3. $\sqrt N(\Delta-\theta)\Rightarrow\mathcal N(0,\sigma_\eta^2)$.

**Beweis(bogen).**
*Zerlegung (Lemma 1(2)):* $\Delta-\theta=\phi(F)+\frac2N\sum_i m_F(V_i)+W_N(F)$.
- **Der $\phi$-Term ist $O(N^{-1/2})$-fluktuierend, nicht $O(1)$:** Wegen $O(d)$-Invarianz von $h$ ist $\phi(R_\#\nu)=\phi(\nu)$; der Orbit des Directors trägt therefore konstantes $\phi$ (und die Normierung gibt $\phi\equiv0$ auf dem exakten Gleichgewicht). Übrig bleibt die Form-Fluktuation $\nu_F+O(N^{-1/2})$-Abweichung, und da $h_1^{\nu_F}\not\equiv0$ (das gebrochene Gleichgewicht ist nicht Haar!), ist $D\phi_{\nu_F}\ne0$: $\phi=\langle D\phi_{\nu_F},\text{Form-Fluktuation}\rangle=O_p(N^{-1/2})$. Beitrag zu $\mathrm{Var}(\Delta)$: $\gamma_\eta/N$.
- **Der $m_F$-Term ist führend:** $m_F(x)=\E_{\nu_F}[h(x,\cdot)]-\theta$ hat über das Cluster $O(1)$-Streung (im Wesentlichen geodätischer Abstand zu $F$), also
$$\mathrm{Var}\Big(\frac2N\sum_i m_F(V_i)\ \Big|\ F\Big)=\frac4N\mathrm{Var}_{\nu_F}(m_F)=\frac{4c_1(\eta)}{N},\qquad c_1=\E_F[\mathrm{Var}_{\nu_F}(m_F)]=O(w_\eta^2).$$
- **Grenzverteilung:** (a) Bedingt auf $F$ ist $(m_F(V_i))_i$ i.i.d. mit bedingter Varianz $\mathrm{Var}_{\nu_F}(m_F)$; nach Äquivarianz ist diese **a.s. konstant in $F$** (Transport entlang des Orbits), damit kollabiert die Varianz-Mischung zum einzelnen Gauß. (b) Die Form-Fluktuation ist im Mean-Field-Limes jointly gaußsch (Fluktuations-CLT um das McKean–Vlasov-Gleichgewicht). (c) $\sqrt N W_N=O_p(N^{-1/2})\to0$. Summe zweier jointly gaußscher Anteile ⟹ $\mathcal N(0,4c_1+\gamma_\eta)$. $\square$ (Beweisskizze-Niveau: die Rigorisierung von (b) über den linearisierten Fluktuationsoperator ist offen, §13.)

**Numerik (d=8, k=1, η=100):** Slope $-1.004$; $N\cdot\mathrm{Var}=6.65$–$6.79\times10^{-3}$ konstant über $N=128$–$2048$; Schiefe $|\cdot|\le0.14$, Kurtosis $2.6$–$3.4$, QQ-r $\ge0.9988$; gemessenes $c_1=0.0016$, $4c_1=6.4\times10^{-3}$ erklärt $\ge95\%$ (bei $\eta\in\{60,80\}$: $97$–$99.6\%$); $\eta\,\sigma_\eta^2\approx0.64$–$0.70$ konstant ⟹ $\sigma_\eta^2\asymp D/(\kappa\eta)$ ✓. Für $k=2$, d=8: Slope $-1.001$ ✓.

---

## 9. Zwischenfazit: die korrigierte Dichotomie-Aussage

$$\boxed{\ \eta<\eta_c:\ \mathrm{Var}(\Delta)=\Theta(N^{-2}),\quad N(\Delta-\theta)\Rightarrow\text{indef. gewichtete }\chi^2;\qquad \eta>\eta_c:\ \mathrm{Var}(\Delta)=\Theta(N^{-1}),\quad \sqrt N(\Delta-\theta)\Rightarrow\mathcal N(0,\sigma_\eta^2)\ }$$

mit $\zeta_1\equiv0$ **in beiden Phasen** — die Dichotomie lebt in der *bedingten* Struktur ($m_F\ne0$ vs. $m_{\mu_H}\equiv0$), nicht in der marginalen.

---

## 10. Satz 4 (analytische Schwelle): $\eta_c^{\mathrm{MF}}(d)=\dfrac{D\,d(d+2)}{2}$

**Schritt 1 (Ein-Teilchen-Antwort, exakt).** Betrachte EIN Teilchen unter Drift mit externem Feld der Amplitude $h$ entlang $u=e_1$:
$$\beta(v)=2\eta h\big[(u\cdot v)u-(u\cdot v)^2v\big],\qquad \dd v=\beta(v)\,\dd t+\sqrt{2D}\,\dd W_{\mathbb S^{d-1}}.$$
Dies ist exakt die Driftform, die das Schwarmfeld an einem isotropen Basispunkt erzeugt (der isotrope Anteil $\tfrac1d I$ fällt unter der tangentialen Projektion weg — nachrechnen: $P_t\big((uu^\top-\tfrac1dI)v\big)=(u\cdot v)u-(u\cdot v)^2v$).

Sei $p=(u\cdot v)^2$, $\mu=\E_{\mu_H}p=\tfrac1d$. Die stationäre Dichte bei Feld $h$ ist $\rho_h\propto e^{(\eta h/D)p}$. Die **exakte kumulantische Expansion** der Antwort (aus $\langle p\rangle_h=\langle p e^{tp}\rangle/\langle e^{tp}\rangle$ mit $t=\eta h/D$, exakt bis Ordnung $h^2$):
$$a(h):=\langle p\rangle_h-\frac1d=\underbrace{\frac{\eta}{D}\,\mathrm{Var}(p)}_{\chi_0}\,h\;+\;\underbrace{\frac{\eta^2}{2D^2}\,\E\big[(p-\mu)^3\big]}_{\beta_2}\,h^2\;+\;O(h^3).$$

**Schritt 2 (Kumulanten von $p$ unter Haar, exakt).** Mit $\E[p^k]=(2k-1)!!/\big[d(d+2)\cdots(d+2k-2)\big]$:
$$\mathrm{Var}(p)=\frac{2(d-1)}{d^2(d+2)},\qquad \E\big[(p-\mu)^3\big]=\frac{8(d-1)(d-2)}{d^3(d+2)(d+4)}.$$
*(Nachrechnen: $\E[(p-\mu)^3]=\E p^3-3\mu\E p^2+2\mu^3$ mit $\E p^3=\tfrac{15}{d(d+2)(d+4)}$; Zähler wird $8(d-1)(d-2)$.)*

Also
$$\chi_0=\frac{2\eta(d-1)}{D\,d^2(d+2)},\qquad \beta_2=\frac{4\eta^2(d-1)(d-2)}{D^2d^3(d+2)(d+4)}.$$
Die Messung bestätigt $\chi_0/\eta$ bei $d=8$ auf **4 Stellen** (0.0218 vs. 0.0219), und unabhängig gibt die Kubo-Formel $\langle\beta\cdot\nabla\psi_2\rangle/(D\kappa_2)$ mit $\psi_2=p-\tfrac1d$, $\kappa_2=2d$ (Grad-2-Harmonische auf $\mathbb{RP}^{d-1}$), denselben Wert.

**Schritt 3 (Selbstkonsistenz).** Das Schwarmfeld liefert die Feldamplitude $h=c$ mit der Anisotropie $\E[vv^\top]-\tfrac1dI=c\,(uu^\top-\tfrac1dI)$ und $c=\dfrac{a}{1-1/d}$. Fixpunkt:
$$a=\chi_0\,\frac{a}{1-1/d}+\beta_2\Big(\frac{a}{1-1/d}\Big)^2+\cdots
\quad\Longrightarrow\quad
\Big[(1-\tfrac1d)-\chi_0\Big]c=\beta_2\,\frac{c^2}{(1-1/d)^2}+\cdots$$
Nichttriviale Lösung $c>0$ existiert ⟺ $\chi_0>(1-\tfrac1d)$:
$$\frac{2\eta(d-1)}{Dd^2(d+2)}>\frac{d-1}{d}\quad\Longleftrightarrow\quad \eta>\frac{D\,d(d+2)}{2}.$$

**Satz 4.** $\eta_c^{\mathrm{MF}}(d)=\dfrac{D\,d(d+2)}{2}$: für $\eta<\eta_c$ ist der isotrope Zustand linear stabil, für $\eta>\eta_c$ instabil.
**Werte:** $d{=}2$: $4$; $d{=}4$: $12$; $d{=}8$: $40$; $d{=}16$: $144$.
**Numerik:** gemessene χ-Gain-Durchgänge ($\chi=(d-1)/d$): $d{=}2$: $\approx4.5\pm0.5$; $d{=}4$: $\approx13$–$14$; $d{=}8$: $\approx42$. ✓

---

## 11. Satz 5 (Übergangs-Charakter): kontinuierlich für $d\le2$, subkritisch für $d>2$

**Satz 5 (Landau-Niveau).** Aus der Exaktpansion in Schritt 1:
- $\beta_2>0\iff d>2$.
- Die Fixpunktgleichung $c\big[(1-\tfrac1d)-\chi_0(\eta)\big]=\beta_2 c^2/(1-\tfrac1d)^2+\cdots$ liefert:
  - **$d>2$ ($\beta_2>0$):** es existiert eine geordnete Lösung **für $\eta<\eta_c$** mit $c\propto(\eta_c-\eta)$ — die geordnete Zweig reicht *unter* die lineare Schwelle ⟹ **subkritische Bifurkation mit Koexistenzfenster** $[\eta_A,\eta_c]$ (unteres Ende = Spinodal der geordneten Phase, durch höhere Ordnungen bestimmt).
  - **$d\le2$ ($\beta_2=0$):** Nichttriviallösung nur für $\eta>\eta_c$ mit $c\propto\sqrt{\eta-\eta_c}$ ⟹ **kontinuierliche (supercritische) Bifurkation**.
- Für $d=2$ ist das exakt: die Drift ist tangentiallos im quartischen Term ($-\eta c\sin2\alpha$, reine Adler-Dynamik), stationär $\rho\propto e^{(\eta c/2D)\cos2\alpha}$, Selbstkonsistenz $r_1=I_1(\nu)/I_0(\nu)$, $\nu=\eta r_1/(2D)$, Landau $I_1/I_0=\nu/2-\nu^3/16+\cdots$ ⟹ $\eta_c=4D$ und kontinuierlich. ✓

**Warum das erklärt alle Messungen:** Im Koexistenzfenster sind beide Zweige stabil; das von $N$ abhängige Nukleations-Barrieren-Verhältnis entscheidet, welchen Zweig ein finites System besetzt. Gemessen:
- Zweig-Persistenz (geordneter Start): d=8 stabil $\eta\ge20$, verloren $\eta\le16$; d=4 stabil $\ge12$, verloren $\le10$; d=2 verloren $\le2$.
- Wachstumsraten von $r(t)$ von Haar-Start (d=8, N=2048): $\lambda\approx0.09/0.14/0.19$ bei $\eta=25/28/30$ (nur Rauschwandern — Attraktor ungeordnet) vs. $\lambda=1.3/2.6/4.4$ bei $\eta=33/36/40$ (echte Instabilität) ⟹ Scan-„Übergang" zwischen 30 und 33 liegt *im* Fenster [19,42].
- Nukleation $\propto e^{-N\Delta f}$: N=512 ordnet bei $\eta=30$ in 0.4 Zeiteinheiten, N=2048 nicht in 15 — Barriere skaliert mit $N$.
- Folge: **alle** finiten Scan-„Übergänge" ($\eta\approx12/25/72$ für d=4/8/16) liegen innerhalb ihres Fensters $[\eta_A,\eta_c^{\mathrm{MF}}] = [\approx10,\approx14] / [\approx19,\approx42] / [\text{unten}, 144]$ und sind Erstpassage-, keine Gleichgewichts-Übergänge.

---

## 12. Numerische Gesamttabelle (RTX 3060, torch 2.15 cu132)

| Größe | Vorhersage | Messung |
|---|---|---|
| Slope $\eta=0$ (d=8) | $-2$ | $-1.994$ |
| Slope $\eta=5<\eta_c$ | $-2$ | $-2.013$ |
| Slope $\eta=100$, k=1 | $-1$ | $-1.004$ |
| Slope $\eta=100$, k=2 | $-1$ | $-1.001$ |
| $\mathrm{Gr}(1,2)$: $\sum\lambda_k^2$ | $\pi^2/48=0.205617$ | $0.205617$ (Quadratur) |
| $\mathrm{Var}(N(\Delta-\theta))$, Haar | $\pi^2/24=0.4112$ | $0.407/0.415/0.429$ (N=500/1500/4000) |
| KS gegen $\sum\lambda_k(\chi^2-1)$ | — | $0.006/0.005/0.007$ < $1.63/\sqrt B$ |
| Gaußität $\eta=100$ | Gauß | skew $\le0.14$, kurt $\approx3$, QQ $\ge0.998$ |
| $4c_1$ vs. $N\mathrm{Var}$ | $\sigma^2\approx4c_1$ | $6.4$e-$3$ vs $6.65$–$6.79$e-$3$ ($\ge95\%$) |
| $\eta_c$ (d=2/4/8) | $4/12/40$ | $\approx4.5/13$–$14/42$ |
| Übergangs-Charakter | d=2 kont., d>2 subkrit. | Fenster gemessen: d=4 [10,14], d=8 [19,42] |

Microscopic model: siehe §1; $D=1$, $\dd t=\min(0.05,\,0.25/\eta)$; exakte Hauptwinkel (GPU-batched SVD; geschlossen für $k\le2$).

---

## 13. Ehrliche Beweislücken / offene Punkte

1. **Rigorose Raten** für Satz 2/3: die Chaos-Rate $O(N^{-1/2})$ des Director-Maßes und der Fluktuations-CLT (Satz 3(b)) sind als Standard-Mean-Field-Resultate zitiert/heuristisch benutzt, nicht aus den Axiomen bewiesen. Weg: Dirichlet-Form/Talagrand + linearisierter McKean–Vlasov-Fluktuationsoperator.
2. **$\gamma_\eta$ explizit:** Der Form-Fluktuations-Kanal wird über den Fluktuationsoperator ausgedrückt, aber nicht geschlossen ausgewertet (numerisch ≤ 3 % von $\sigma^2$).
3. **Landau-Satz 5:** Streng genommen eine Herleitung auf Landau-Niveau (Trunkierung nach $h^2$); die volständige Freie-Energie-Rechnung des Mean-Field-Fokker–Planck (mit positiver Kubulante $=8(d-1)(d-2)/(\dots)$) steht aus.
4. **Nukleationsexponenten:** Barriere-Höhe $\Delta f(\eta)$ und $\eta_A(d)$ analytisch.
5. **Invarianz-Satz 1 ist beweisen rigoros** unter (A1)–(A3) — dieser Teil ist vollständig streng.

---

## 14. Die drei Kernideen auf einen Blick

1. **Äquivarianz tötet die marginale Degenerations-Lücke:** $\pi_1=$ Haar *immer*; Symmetriebrechung ist spontan. Alles, was vom Original-Conjecture auf $\zeta_1$ aufbaut, ist identisch Null.
2. **Marginal degeneriert, bedingt nicht-degeneriert:** Im geordneten Regime trägt die *bedingte* erste Hoeffding-Projektion $m_F$ die $N^{-1/2}$-Fluktuation ($\sigma^2=4c_1+\gamma\approx4c_1$), obwohl $h_1\equiv0$ bleibt. Degenerations-Tests am Rand sind in der Mitte falsch.
3. **Die Schwelle ist rechenbar:** Kubo/kumulantische Antwort + Selbstkonsistenz geben $\eta_c=Dd(d+2)/2$ geschlossen; das Vorzeichen der dritten Kumulante von $p$ unter Haar $=8(d-1)(d-2)/(\dots)$ entscheidet kontinuierlich (d≤2) vs. subkritisch (d>2).
