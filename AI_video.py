import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.animation import FFMpegWriter
import os

# ── Global style ──────────────────────────────────────────────────────────
rcParams = plt.rcParams
rcParams['font.family']           = 'monospace'
rcParams['mathtext.fontset']      = 'cm'          # Computer Modern for LaTeX look
rcParams['text.usetex']           = False         # use internal mathtext
rcParams['mathtext.default']      = 'regular'     # use regular weight for variables

BG      = '#0d1117'
FG      = '#e6edf3'
BLUE    = '#58a6ff'
GREEN   = '#3fb950'
PURPLE  = '#bc8cff'
AMBER   = '#d29922'
RED     = '#f85149'
TEAL    = '#39d353'
COMMENT = '#8b949e'
KEYWORD = '#ff7b72'
STRING  = '#a5d6ff'
DIM     = '#30363d'

W, H   = 16, 9
FPS    = 30

writer = FFMpegWriter(fps=FPS, metadata={'title': 'Spam Classifier'},
                      bitrate=3000,
                      extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])

fig = plt.figure(figsize=(W, H), facecolor=BG)

# ── Helpers ───────────────────────────────────────────────────────────────
def clear():
    fig.clf()
    fig.patch.set_facecolor(BG)

def ax_dark(rect=(0.03, 0.05, 0.94, 0.88)):
    ax = fig.add_axes(rect)
    ax.set_facecolor(BG)
    ax.axis('off')
    return ax

def title_bar(ax, text, y=0.93):
    ax.text(0.5, y, text, transform=ax.transAxes,
            fontsize=22, color=FG, fontweight='bold',
            ha='center', va='center', fontfamily='sans-serif')
    ax.axhline(y - 0.06, color=DIM, linewidth=0.8)

def script_note(ax, text, y=0.04, fontsize=8.5, ha='center', color=COMMENT):
    ax.text(0.5, y, text, transform=ax.transAxes,
            fontsize=fontsize, color=color, ha=ha,
            style='italic', fontfamily='sans-serif',
            linespacing=1.4)

def highlight_box(ax, x, y, w, h, color=BLUE, alpha=0.15, label='', lcolor=None):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.008",
                         linewidth=1.5, edgecolor=color,
                         facecolor=color, alpha=alpha,
                         transform=ax.transAxes, zorder=2)
    ax.add_patch(box)
    if label:
        ax.text(x + w + 0.01, y + h/2, label,
                transform=ax.transAxes, fontsize=9,
                color=lcolor or color, va='center', fontfamily='sans-serif')

# ── Scene 1 : Title (3 s) ─────────────────────────────────────────────────
def scene_title(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 3)

    np.random.seed(42)
    for i in range(60):
        xi, yi = np.random.rand(2)
        alpha = 0.04 + 0.03 * np.sin(t * 2 * np.pi + i)
        ax.plot(xi, yi, 'o', color=BLUE, markersize=3, alpha=alpha,
                transform=ax.transAxes)

    alpha_main = min(1.0, t * 3)
    ax.text(0.5, 0.72,
            'Spam Filtering with a',
            transform=ax.transAxes, fontsize=16,
            color=COMMENT, ha='center', alpha=alpha_main,
            fontfamily='sans-serif')
    ax.text(0.5, 0.55,
            '$\\boldsymbol{Naive\\ Bayes\\ Classifier}$',
            transform=ax.transAxes, fontsize=38,
            color=FG, ha='center', alpha=alpha_main)
    ax.text(0.5, 0.38,
            'CM12002  |  Coursework 2',
            transform=ax.transAxes, fontsize=14,
            color=BLUE, ha='center', alpha=alpha_main,
            fontfamily='sans-serif')

# ── Scene 2 : The Problem (5 s) ───────────────────────────────────────────
def scene_problem(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 5)
    title_bar(ax, 'The Problem: Spam vs Ham')

    sa = min(1.0, t * 4)
    spam_box = FancyBboxPatch((0.05, 0.22), 0.35, 0.60,
                               boxstyle="round,pad=0.02",
                               linewidth=2, edgecolor=RED,
                               facecolor='#1a0a0a', alpha=sa,
                               transform=ax.transAxes)
    ax.add_patch(spam_box)
    ax.text(0.225, 0.87, '$\\mathrm{SPAM}$', transform=ax.transAxes,
            fontsize=18, color=RED, ha='center', fontweight='bold', alpha=sa)
    for i, line in enumerate(['FREE money!!!', "You've WON a prize",
                              'Click NOW', 'Cheap meds']):
        ax.text(0.225, 0.75 - i*0.12, line, transform=ax.transAxes,
                fontsize=12, color='#ff9999', ha='center', alpha=sa,
                fontfamily='sans-serif')

    ha_ = min(1.0, max(0, (t - 0.2) * 4))
    ham_box = FancyBboxPatch((0.60, 0.22), 0.35, 0.60,
                              boxstyle="round,pad=0.02",
                              linewidth=2, edgecolor=GREEN,
                              facecolor='#0a1a0a', alpha=ha_,
                              transform=ax.transAxes)
    ax.add_patch(ham_box)
    ax.text(0.775, 0.87, '$\\mathrm{HAM}$', transform=ax.transAxes,
            fontsize=18, color=GREEN, ha='center', fontweight='bold', alpha=ha_)
    for i, line in enumerate(['Meeting at 3pm', 'Your order shipped',
                              'Newsletter update', 'Hi, how are you?']):
        ax.text(0.775, 0.75 - i*0.12, line, transform=ax.transAxes,
                fontsize=12, color='#99ff99', ha='center', alpha=ha_,
                fontfamily='sans-serif')

    ma = min(1.0, max(0, (t - 0.5) * 4))
    mid_box = FancyBboxPatch((0.38, 0.35), 0.24, 0.35,
                              boxstyle="round,pad=0.02",
                              linewidth=2, edgecolor=AMBER,
                              facecolor='#1a1500', alpha=ma,
                              transform=ax.transAxes)
    ax.add_patch(mid_box)
    ax.text(0.5, 0.75, '50% off!', transform=ax.transAxes,
            fontsize=13, color=AMBER, ha='center', alpha=ma, fontfamily='sans-serif')
    ax.text(0.5, 0.63, 'Limited offer', transform=ax.transAxes,
            fontsize=11, color=AMBER, ha='center', alpha=ma, fontfamily='sans-serif')
    ax.text(0.5, 0.51, 'Act fast', transform=ax.transAxes,
            fontsize=11, color=AMBER, ha='center', alpha=ma, fontfamily='sans-serif')
    ax.text(0.5, 0.38, '--- Which is this? ---', transform=ax.transAxes,
            fontsize=10, color=COMMENT, ha='center', alpha=ma,
            style='italic', fontfamily='sans-serif')

# ── Scene 3 : Method Comparison (8 s) ─────────────────────────────────────
def scene_method_compare(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 8)
    title_bar(ax, 'Choosing an Algorithm')

    methods = [
        ('$k$-Nearest Neighbors',
         ['Simple, no training', 'Handles non‑linear'],
         ['Slow prediction (distances)', 'Curse of dimensionality', 'Memory heavy'],
         RED),
        ('Logistic Regression',
         ['Probabilistic output', 'Interpretable coefficients'],
         ['Linear decision boundary', 'Sensitive to outliers'],
         AMBER),
        ('Neural Network',
         ['Can model complex patterns', 'Scalable with data'],
         ['Many hyperparameters', 'Needs large data', 'Black box'],
         RED),
        ('Naïve Bayes (Bernoulli)',
         ['Extremely fast (train & predict)', 'Built‑in uncertainty', 'Works well on small text data'],
         ['Independence assumption (naïve)', 'Binary features only'],
         GREEN),
    ]

    row_h = 0.14
    col1_x = 0.07
    col2_x = 0.38
    col3_x = 0.68
    start_y = 0.78

    ax.text(col1_x + 0.10, 0.88, 'Algorithm', fontsize=12, color=BLUE, ha='center', fontweight='bold')
    ax.text(col2_x + 0.10, 0.88, 'Pros', fontsize=12, color=GREEN, ha='center', fontweight='bold')
    ax.text(col3_x + 0.10, 0.88, 'Cons', fontsize=12, color=RED, ha='center', fontweight='bold')

    for i, (name, pros, cons, col) in enumerate(methods):
        alpha = min(1.0, max(0, (t - i*0.15) * 4))
        y = start_y - i*row_h
        ax.text(col1_x, y, name, transform=ax.transAxes,
                fontsize=12, color=col, fontweight='bold', alpha=alpha, va='top')
        for j, p in enumerate(pros):
            ax.text(col2_x, y - j*0.04, '✓ ' + p, transform=ax.transAxes,
                    fontsize=9, color=GREEN, alpha=alpha, va='top')
        for j, c in enumerate(cons):
            ax.text(col3_x, y - j*0.04, '✗ ' + c, transform=ax.transAxes,
                    fontsize=9, color=RED, alpha=alpha, va='top')

    # Animated scanner effect
    scan_progress = min(1.0, t * 1.5)          # scan takes ~5.3s of the 8s scene
    num_rows = len(methods)
    # scanning from top (row 0) to bottom (row 3)
    raw_idx = scan_progress * (num_rows - 1)   # 0 to 3
    idx = int(raw_idx)
    frac = raw_idx - idx
    # interpolate y position between rows
    y_top = start_y - idx*row_h
    y_bot = start_y - (idx+1)*row_h
    scan_y = y_top + frac * (y_bot - y_top) - 0.02   # small offset to align text

    # Draw a moving highlight (thick semi‑transparent border)
    scan_box = FancyBboxPatch((0.06, scan_y), 0.92, row_h+0.02,
                              boxstyle="round,pad=0.008",
                              linewidth=2.5, edgecolor='#ffffff', facecolor='none',
                              alpha=0.7, transform=ax.transAxes, zorder=3)
    ax.add_patch(scan_box)

    # After scan is complete (t > 0.75), show the final settled green box
    if t > 0.75:
        a = min(1.0, (t-0.75)*5)
        highlight_box(ax, 0.06, start_y-3*row_h-0.02, 0.92, row_h+0.02,
                      GREEN, alpha=a, label='', lcolor=GREEN)
        # remove the scanner once settled
        scan_box.set_alpha(0.0)

# ── Scene 4 : Dataset Shape (6 s) ─────────────────────────────────────────
def scene_dataset_shape(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 6)
    title_bar(ax, 'The Dataset')

    ax.text(0.5, 0.82,
            'Training set: (1000, 55)          Test set: (500, 55)',
            transform=ax.transAxes, fontsize=18, color=FG, ha='center',
            fontfamily='monospace')

    data_lines = [
        '[[1 0 0 ... 1 1 1]',
        ' [1 1 0 ... 1 1 1]',
        ' [0 0 0 ... 0 0 0]',
        ' ...',
        ' [0 0 0 ... 0 0 0]',
        ' [0 0 0 ... 1 0 0]',
        ' [0 0 0 ... 1 0 0]]',
    ]
    for i, line in enumerate(data_lines):
        alpha = min(1.0, max(0, (t - 0.3 - i*0.04) * 6))
        ax.text(0.5, 0.62 - i*0.06, line, transform=ax.transAxes,
                fontsize=12, color=COMMENT, alpha=alpha, ha='center',
                fontfamily='monospace')

# ── Scene 5 : Formula (7 s) ───────────────────────────────────────────────
def scene_formula(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 7)
    title_bar(ax, 'Naïve Bayes – The Formula')

    steps = [
        (0.00, '$P(\\mathrm{spam} \\mid \\boldsymbol{x}) = P(\\mathrm{spam}) \\prod_{i=1}^{54} P(x_i \\mid \\mathrm{spam})$', BLUE, 20),
        (0.20, '1.  $\\boldsymbol{Prior}$: how common spam is overall',                                                              PURPLE, 16),
        (0.33, '2.  $\\boldsymbol{Likelihood}$: how often keyword $i$ appears in spam',                                                 TEAL, 16),
        (0.46, '3.  $\\boldsymbol{Product\\ over\\ 54\\ keywords}$',                                                                 GREEN, 16),
        (0.58, '4.  Take $\\log$ $\\rightarrow$ sum $\\log$-probabilities (avoids underflow)',                                     AMBER, 16),
        (0.70, '5.  Predict spam if $\\log P(\\mathrm{spam} \\mid \\boldsymbol{x}) > \\log P(\\mathrm{ham} \\mid \\boldsymbol{x})$',        RED, 16),
    ]

    for i, (thresh, text, col, fs) in enumerate(steps):
        alpha = min(1.0, max(0, (t - thresh) * 5))
        y = 0.82 - i * 0.14
        if i == 0:
            box = FancyBboxPatch((0.04, y - 0.10), 0.92, 0.25,
                                 boxstyle="round,pad=0.01",
                                 linewidth=1.5, edgecolor=BLUE,
                                 facecolor='#0d1f3c', alpha=alpha * 0.9,
                                 transform=ax.transAxes)
            ax.add_patch(box)
            ax.text(0.5, y - 0.02, text, transform=ax.transAxes,
                    fontsize=fs, color=col, ha='center', va='center', alpha=alpha)
        else:
            ax.text(0.08, y, text, transform=ax.transAxes,
                    fontsize=fs, color=col, alpha=alpha, fontfamily='sans-serif')


# ── Scene 6 : Bernoulli Visualisation (8 s) ───────────────────────────────
def scene_bernoulli(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 8)
    title_bar(ax, 'Bernoulli Naïve Bayes – Binary Features')

    keywords = ['free', 'money', 'winner', 'meeting', 'invoice', 'click', 'order', 'prize']
    spam_p   = [0.82,   0.74,    0.68,     0.12,      0.21,      0.77,   0.15,    0.71]
    ham_p    = [0.18,   0.19,    0.06,     0.61,      0.55,      0.14,   0.64,    0.05]
    email    = [1,       1,       0,        0,          0,         0,      0,       1]

    bar_w = 0.04
    gap   = 0.10
    x0    = 0.08

    for i, (kw, sp, hp, em) in enumerate(zip(keywords, spam_p, ham_p, email)):
        x = x0 + i * gap
        prog = min(1.0, max(0, (t - i * 0.08) * 5))

        bh_s = 0.42 * sp * prog
        col_s = RED if em else '#662222'
        ax.add_patch(FancyBboxPatch((x, 0.20), bar_w, bh_s,
                                    boxstyle="square,pad=0",
                                    facecolor=col_s, alpha=0.85 if em else 0.4,
                                    transform=ax.transAxes))
        bh_h = 0.42 * hp * prog
        col_h = GREEN if em else '#224422'
        ax.add_patch(FancyBboxPatch((x + bar_w + 0.002, 0.20), bar_w, bh_h,
                                    boxstyle="square,pad=0",
                                    facecolor=col_h, alpha=0.85 if em else 0.4,
                                    transform=ax.transAxes))
        ax.text(x + bar_w + 0.001, 0.11, kw, transform=ax.transAxes,
                fontsize=10, color=FG if em else COMMENT,
                ha='center', rotation=30, fontfamily='monospace')

        if em:
            ax.text(x + bar_w + 0.001, 0.68, '[present]', transform=ax.transAxes,
                    fontsize=9, color=AMBER, ha='center', alpha=prog,
                    fontfamily='sans-serif')

    ax.add_patch(FancyBboxPatch((0.06, 0.78), 0.14, 0.05,
                                 boxstyle="round,pad=0.01", facecolor=RED, alpha=0.6,
                                 transform=ax.transAxes))
    ax.text(0.22, 0.805, '$P(\\mathrm{keyword}\\mid\\mathrm{spam})$', transform=ax.transAxes,
            fontsize=12, color=RED)
    ax.add_patch(FancyBboxPatch((0.48, 0.78), 0.14, 0.05,
                                 boxstyle="round,pad=0.01", facecolor=GREEN, alpha=0.6,
                                 transform=ax.transAxes))
    ax.text(0.64, 0.805, '$P(\\mathrm{keyword}\\mid\\mathrm{ham})$', transform=ax.transAxes,
            fontsize=12, color=GREEN)
    ax.text(0.5, 0.90, '[present] = keyword found in this email', transform=ax.transAxes,
            fontsize=11, color=AMBER, ha='center', fontfamily='sans-serif')

    if t > 0.5:
        a = min(1.0, (t-0.5)*3)
        ax.text(0.08, 0.04,
                '$\\boldsymbol{Naïve\\ assumption:}$ "free", "money", "winner" independent given spam – unrealistic but fast.',
                transform=ax.transAxes, fontsize=11, color=AMBER, alpha=a, fontfamily='sans-serif')
        ax.text(0.08, 0.00,
                '$\\boldsymbol{Latency:}$ prediction is $\\mathcal{O}(n_\\mathrm{features})$ = 54 dot products $\\rightarrow$ <0.1 ms/email.',
                transform=ax.transAxes, fontsize=11, color=GREEN, alpha=a, fontfamily='sans-serif')

# ── Scene 7 : Training Step 1 (5 s) ───────────────────────────────────────
def scene_train1(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 5)
    title_bar(ax, 'Training – Step 1: Separating Labels and Features')

    lines = [
        ('def train(self, data):',                      KEYWORD),
        ('    # Separate labels and features',           COMMENT),
        ('    labels   = data[:, 0]',                   FG),
        ('    features = data[:, 1:]',                  FG),
        ('',                                            FG),
        ('    n_features = features.shape[1]  # = 54',  COMMENT),
        ('',                                            FG),
        ('    spam_emails = features[labels == 1]',     GREEN),
        ('    ham_emails  = features[labels == 0]',     BLUE),
    ]

    alpha_code = min(1.0, t * 3)
    for i, (text, col) in enumerate(lines):
        ax.text(0.08, 0.82 - i * 0.072, text, transform=ax.transAxes,
                fontsize=12, color=col, alpha=alpha_code,
                va='center', fontfamily='monospace')

    if t > 0.4:
        a = min(1.0, (t - 0.4) * 4)
        highlight_box(ax, 0.07, 0.655, 0.45, 0.05, RED, alpha=0.12,
                      label='  column 0: spam=1, ham=0', lcolor=RED)
        highlight_box(ax, 0.07, 0.583, 0.45, 0.05, BLUE, alpha=0.12,
                      label='  columns 1-54: keyword features', lcolor=BLUE)

# ── Scene 8 : Training Step 2 – Priors (5 s) ──────────────────────────────
def scene_train2(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 5)
    title_bar(ax, 'Training – Step 2: Prior Probabilities')

    lines = [
        ('    # Prior probabilities: log P(spam), log P(ham)',  COMMENT),
        ('    total = len(labels)',                               FG),
        ('    self.log_prior_spam = np.log(',                     KEYWORD),
        ('        len(spam_emails) / total)',                      GREEN),
        ('    self.log_prior_ham  = np.log(',                     KEYWORD),
        ('        len(ham_emails)  / total)',                      BLUE),
        ('    ',                                                 KEYWORD),
    ]

    for i, (text, col) in enumerate(lines):
        alpha = min(1.0, max(0, (t - i * 0.07) * 5))
        ax.text(0.08, 0.82 - i * 0.073, text, transform=ax.transAxes,
                fontsize=12, color=col, alpha=alpha,
                va='center', fontfamily='monospace')

    if t > 0.5:
        a = min(1.0, (t - 0.5) * 3)
        ax_inset = fig.add_axes([0.65, 0.35, 0.28, 0.38])
        ax_inset.set_facecolor('#161b22')
        for spine in ax_inset.spines.values():
            spine.set_color(DIM)
        spam_frac = 0.394
        ax_inset.bar(['Spam', 'Ham'], [spam_frac * a, (1 - spam_frac) * a],
                     color=[RED, GREEN], alpha=0.8, width=0.5)
        ax_inset.set_ylim(0, 1)
        ax_inset.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_inset.tick_params(colors=COMMENT, labelsize=9)
        ax_inset.set_title('$\\log P(\\mathrm{class})$', color=FG, fontsize=10, pad=5)
        ax_inset.text(0, spam_frac * a + 0.03, '39.4%', ha='center',
                      color=RED, fontsize=9, fontweight='bold')
        ax_inset.text(1, (1 - spam_frac) * a + 0.03, '60.6%', ha='center',
                      color=GREEN, fontsize=9, fontweight='bold')

# ── Scene 9 : Training Step 3 – Likelihoods + Laplace (7 s) ───────────────
def scene_train3(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 7)
    title_bar(ax, 'Training – Step 3: Likelihoods + Laplace Smoothing')

    lines = [
        ('    self.log_likelihood_spam = np.log(',             KEYWORD),
        ('        (spam_emails.sum(axis=0) + self.k)',         GREEN),
        ('        / (len(spam_emails) + 2 * self.k))',          GREEN),
        ('    self.log_likelihood_ham  = np.log(',             KEYWORD),
        ('        (ham_emails.sum(axis=0)  + self.k)',         BLUE),
        ('        / (len(ham_emails)  + 2 * self.k))',          BLUE),
    ]

    for i, (text, col) in enumerate(lines):
        alpha = min(1.0, max(0, (t - i * 0.07) * 5))
        ax.text(0.08, 0.83 - i * 0.073, text, transform=ax.transAxes,
                fontsize=11.5, color=col, alpha=alpha,
                va='center', fontfamily='monospace')

    if t > 0.45:
        a = min(1.0, (t - 0.45) * 3)
        lbox = FancyBboxPatch((0.06, 0.08), 0.88, 0.25,
                               boxstyle="round,pad=0.01",
                               linewidth=1.5, edgecolor=AMBER,
                               facecolor='#1a1500', alpha=a * 0.9,
                               transform=ax.transAxes)
        ax.add_patch(lbox)
        ax.text(0.5, 0.30,
                'Without Laplace ($k=0$): if a keyword never appears in spam  $\\rightarrow P=0 \\rightarrow$ score = 0',
                transform=ax.transAxes, fontsize=12, color=RED,
                ha='center', alpha=a, fontfamily='sans-serif')
        ax.text(0.5, 0.22,
                'With Laplace ($k=1$): add 1 to every count  $\\rightarrow$ no probability is ever exactly zero',
                transform=ax.transAxes, fontsize=12, color=GREEN,
                ha='center', alpha=a, fontfamily='sans-serif')
        ax.text(0.5, 0.14,
                '$P(\\mathrm{feature}\\mid\\mathrm{spam}) = \\frac{\\mathrm{count} + k}{n_\\mathrm{spam} + 2k}$',
                transform=ax.transAxes, fontsize=14, color=AMBER,
                ha='center', alpha=a)

# ── Scene 10 : Laplace Visualisation (7 s) ────────────────────────────────
def scene_laplace(f):
    clear()
    t = f / (FPS * 7)
    title_ax = ax_dark((0.03, 0.85, 0.94, 0.12))
    title_bar(title_ax, 'Laplace Smoothing – How It Works', y=0.5)

    ax1 = fig.add_axes([0.05, 0.15, 0.40, 0.65])
    ax1.set_facecolor('#161b22')
    for sp in ax1.spines.values(): sp.set_color(DIM)
    ax1.tick_params(colors=COMMENT, labelsize=8)

    probs_raw = np.abs(np.random.RandomState(7).randn(10) * 0.1) + 0.05
    probs_raw[3] = 0.0

    prog = min(1.0, t * 3)
    cols = [RED if p == 0 else '#4444aa' for p in probs_raw]
    ax1.bar(range(10), probs_raw * prog, color=cols, alpha=0.8)
    ax1.set_title('Without smoothing ($k=0$)', color=RED, fontsize=11, pad=6)
    ax1.set_xlabel('Keyword index', color=COMMENT, fontsize=9)
    ax1.set_ylabel('$P(\\mathrm{keyword}\\mid\\mathrm{spam})$', color=COMMENT, fontsize=9)
    ax1.set_ylim(0, 0.35)
    ax1.text(3, 0.02, '$P=0$', ha='center', color=RED, fontsize=10, fontweight='bold')
    ax1.text(4.5, 0.28,
             'One zero keyword\n$\\rightarrow$ whole product = 0\n$\\rightarrow$ prediction fails',
             color=RED, fontsize=9, ha='center',
             bbox=dict(facecolor='#2a0a0a', edgecolor=RED, boxstyle='round'))

    ax2 = fig.add_axes([0.55, 0.15, 0.40, 0.65])
    ax2.set_facecolor('#161b22')
    for sp in ax2.spines.values(): sp.set_color(DIM)
    ax2.tick_params(colors=COMMENT, labelsize=8)

    k = 1
    counts = np.array([8, 4, 12, 0, 7, 3, 9, 1, 6, 5], dtype=float)
    n_spam = 40
    probs_smooth = (counts + k) / (n_spam + 2 * k)

    if t > 0.3:
        prog2 = min(1.0, (t - 0.3) * 3)
        ax2.bar(range(10), probs_smooth * prog2, color=GREEN, alpha=0.8)
        ax2.set_title('With Laplace smoothing ($k=1$)', color=GREEN, fontsize=11, pad=6)
        ax2.set_xlabel('Keyword index', color=COMMENT, fontsize=9)
        ax2.set_ylim(0, 0.35)
        ax2.bar([3], [probs_smooth[3] * prog2], color=AMBER, alpha=0.9)
        ax2.text(3, probs_smooth[3] + 0.02,
                 f'{probs_smooth[3]:.3f}', ha='center', color=AMBER, fontsize=9)
        ax2.text(4.5, 0.28,
                 f'$(0 + {k}) / ({n_spam} + {2*k})$\n= {probs_smooth[3]:.3f}\n$\\rightarrow$ never zero',
                 color=GREEN, fontsize=9, ha='center',
                 bbox=dict(facecolor='#0a2a0a', edgecolor=GREEN, boxstyle='round'))

    fig.text(0.5, 0.04,
             '"Laplace smoothing adds a pseudocount $k$ to every keyword,\n'
             ' ensuring no probability is ever exactly zero."',
             fontsize=8.5, color=COMMENT, ha='center', style='italic',
             fontfamily='sans-serif')

# ── Scene 11 : Absent Features (6 s) ──────────────────────────────────────
def scene_absent(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 6)
    title_bar(ax, 'Optimisation – Modelling Absent Features')

    lines = [
        ('    # Probability of a feature being ABSENT',              COMMENT),
        ('    self.log_likelihood_spam_0 = np.log(',                 KEYWORD),
        ('        1 - np.exp(self.log_likelihood_spam))',              PURPLE),
        ('    self.log_likelihood_ham_0  = np.log(',                 KEYWORD),
        ('        1 - np.exp(self.log_likelihood_ham))',               TEAL),
        ('    ',                                                     KEYWORD),
    ]

    for i, (text, col) in enumerate(lines):
        alpha = min(1.0, max(0, (t - i * 0.08) * 5))
        ax.text(0.08, 0.83 - i * 0.078, text, transform=ax.transAxes,
                fontsize=12, color=col, alpha=alpha,
                va='center', fontfamily='monospace')

    if t > 0.5:
        a = min(1.0, (t - 0.5) * 3)
        ibox = FancyBboxPatch((0.06, 0.10), 0.88, 0.30,
                               boxstyle="round,pad=0.01",
                               linewidth=1.5, edgecolor=PURPLE,
                               facecolor='#150d2a', alpha=a * 0.9,
                               transform=ax.transAxes)
        ax.add_patch(ibox)
        ax.text(0.5, 0.38,
                'Most implementations only score keywords that ARE present.',
                transform=ax.transAxes, fontsize=14, color=RED,
                ha='center', alpha=a, fontfamily='sans-serif')
        ax.text(0.5, 0.28,
                'But absent keywords are evidence too.',
                transform=ax.transAxes, fontsize=14, color=AMBER,
                ha='center', alpha=a, fontfamily='sans-serif')
        ax.text(0.5, 0.18,
                'If "free" is absent $\\rightarrow$ nudges prediction toward ham.',
                transform=ax.transAxes, fontsize=14, color=GREEN,
                ha='center', alpha=a, fontfamily='sans-serif')

# ── Scene 12 : Predict (5 s) ──────────────────────────────────────────────
def scene_predict(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 5)
    title_bar(ax, 'Predicting – Scoring Each Email')

    lines = [
        ('def predict(self, data):',                                         KEYWORD),
        ('    log_prob_spam = (',                                             FG),
        ('        self.log_prior_spam',                                       PURPLE),
        ('        + (data * self.log_likelihood_spam).sum(axis=1)',           GREEN),
        ('        + ((1-data) * self.log_likelihood_spam_0).sum(axis=1))',     GREEN),
        ('    log_prob_ham = (',                                              FG),
        ('        self.log_prior_ham',                                        PURPLE),
        ('        + (data * self.log_likelihood_ham).sum(axis=1)',            BLUE),
        ('        + ((1-data) * self.log_likelihood_ham_0).sum(axis=1))',      BLUE),
        ('    return (log_prob_spam > log_prob_ham).astype(int)',             AMBER),
    ]

    for i, (text, col) in enumerate(lines):
        alpha = min(1.0, max(0, (t - i * 0.05) * 5))
        ax.text(0.05, 0.80 - i * 0.058, text, transform=ax.transAxes,
                fontsize=10.5, color=col, alpha=alpha,
                va='center', fontfamily='monospace')

    # Highlight boxes removed as requested
    # if t > 0.7: ... (no highlight boxes)

# ── Scene 13 : Results (7 s) ──────────────────────────────────────────────
def scene_results(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 7)
    title_bar(ax, 'Results & Accuracy')

    acc_alpha = min(1.0, t * 3)

    # Smaller pie chart placed lower and behind
    if acc_alpha > 0.1:
        pie_ax = fig.add_axes([0.35, 0.53, 0.30, 0.25], facecolor=BG)
        pie_ax.set_zorder(0)                     # push pie behind main axes
        pie_ax.pie([89, 11],
                    colors=[TEAL, '#1a2a1a'],
                    startangle=90,
                    counterclock=False,
                    wedgeprops={'edgecolor': BG, 'linewidth': 2},
                    explode=[0.03, 0])
        centre_circle = plt.Circle((0, 0), 0.7, color=BG, fc=BG)  # slightly larger hole
        pie_ax.add_artist(centre_circle)
        pie_ax.set_xlim(-1.2, 1.2)
        pie_ax.set_ylim(-1.2, 1.2)
        pie_ax.axis('off')

    # Ensure main axes are in front
    ax.set_zorder(1)

    # Large 89% text centred over the donut
    ax.text(0.5, 0.72, '$\\boldsymbol{89\\%}$', transform=ax.transAxes,
            fontsize=72, color=TEAL, ha='center', fontweight='bold',
            alpha=acc_alpha)

    # Subtitle
    ax.text(0.5, 0.60, 'accuracy on 500‑email test set',
            transform=ax.transAxes, fontsize=14,
            color=FG, ha='center', alpha=acc_alpha, fontfamily='sans-serif')

    if t > 0.35:
        a = min(1.0, (t - 0.35) * 3)

        # --- Strengths box ---
        strength_box = FancyBboxPatch((0.05, 0.08), 0.42, 0.42,
                                       boxstyle="round,pad=0.02",
                                       linewidth=1.5, edgecolor=GREEN,
                                       facecolor='#0a1a0a', alpha=a * 0.9,
                                       transform=ax.transAxes)
        ax.add_patch(strength_box)
        # Title moved higher and bigger
        ax.text(0.26, 0.55, '$\\boldsymbol{Strengths}$', transform=ax.transAxes,
                fontsize=16, color=GREEN, fontweight='bold', alpha=a,
                ha='center', fontfamily='sans-serif')

        strengths = ['Trains in $<$ 1 ms',
                     'Built from scratch – NumPy only',
                     'Models absent features explicitly',
                     'Interpretable log‑probabilities']
        for i, s in enumerate(strengths):
            ax.text(0.07, 0.44 - i * 0.09, '$\\checkmark$  ' + s, transform=ax.transAxes,
                    fontsize=12, color=GREEN, alpha=a, fontfamily='sans-serif')

        # --- Limitations box ---
        limits_box = FancyBboxPatch((0.53, 0.08), 0.42, 0.42,
                                      boxstyle="round,pad=0.02",
                                      linewidth=1.5, edgecolor=RED,
                                      facecolor='#1a0a0a', alpha=a * 0.9,
                                      transform=ax.transAxes)
        ax.add_patch(limits_box)
        # Title moved higher and bigger
        ax.text(0.74, 0.55, '$\\boldsymbol{Limitations}$', transform=ax.transAxes,
                fontsize=16, color=RED, fontweight='bold', alpha=a,
                ha='center', fontfamily='sans-serif')

        limits = ['Independence assumption',
                  'Binary only – ignores term frequency',
                  'Fixed 54‑word vocabulary',
                  'Linear decision boundary']
        for i, s in enumerate(limits):
            ax.text(0.55, 0.44 - i * 0.09, '$\\times$  ' + s, transform=ax.transAxes,
                    fontsize=12, color=RED, alpha=a, fontfamily='sans-serif')

# ── Scene 14 : Neural Networks & Future Work (10 s) ───────────────────────
def scene_nn_future(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 10)
    title_bar(ax, 'Beyond 89% – Where Next?')

    if t > 0.15:
        a1 = min(1.0, (t-0.15)*3)
        
        analysis_box = FancyBboxPatch((0.05, 0.38), 0.90, 0.48,
                                       boxstyle="round,pad=0.02",
                                       linewidth=1.5, edgecolor=BLUE,
                                       facecolor='#0d1f3c', alpha=a1 * 0.85,
                                       transform=ax.transAxes)
        ax.add_patch(analysis_box)
        
        ax.text(0.5, 0.82, 'Analysis', transform=ax.transAxes,
                fontsize=16, color=BLUE, fontweight='bold', alpha=a1,
                ha='center', fontfamily='sans-serif')
        
        ax.text(0.08, 0.74,
                'My classifier achieved 89% accuracy on the held-out test set – good, but improvable.',
                transform=ax.transAxes, fontsize=13, color=FG, alpha=a1,
                fontfamily='sans-serif', linespacing=1.5)
        
        ax.text(0.08, 0.65,
                '$\\boldsymbol{Limitation\\ 1:}$ Independence assumption\n'
                'Treats every keyword as unrelated. In reality, spam words like\n'
                '"free" and "money" cluster together – the model misses these patterns.',
                transform=ax.transAxes, fontsize=12, color=RED, alpha=a1,
                fontfamily='sans-serif', linespacing=1.4)
        
        ax.text(0.08, 0.53,
                '$\\boldsymbol{Limitation\\ 2:}$ Binary presence only\n'
                'Only captures whether a word appears, not how often.\n'
                'Valuable frequency information is thrown away.',
                transform=ax.transAxes, fontsize=12, color=AMBER, alpha=a1,
                fontfamily='sans-serif', linespacing=1.4)

    if t > 0.45:
        a2 = min(1.0, (t-0.45)*4)
        
        solution_box = FancyBboxPatch((0.05, 0.05), 0.90, 0.28,
                                       boxstyle="round,pad=0.02",
                                       linewidth=2.5, edgecolor=TEAL,
                                       facecolor='#0a1a1a', alpha=a2 * 0.9,
                                       transform=ax.transAxes)
        ax.add_patch(solution_box)
        
        ax.text(0.5, 0.30, 'The Path Forward', transform=ax.transAxes,
                fontsize=14, color=TEAL, fontweight='bold', alpha=a2,
                ha='center', fontfamily='sans-serif')
        
        ax.text(0.08, 0.22,
                '$\\boldsymbol{Neural\\ networks}$ can learn the non-linear relationships\n'
                'between features that Naïve Bayes is fundamentally unable to model.',
                transform=ax.transAxes, fontsize=12, color=GREEN, alpha=a2,
                fontfamily='sans-serif', linespacing=1.5)
        
        ax.text(0.08, 0.12,
                'With more data, they could capture complex spam patterns – word clusters,\n'
                'context, and frequency – pushing accuracy well beyond 89%.',
                transform=ax.transAxes, fontsize=12, color=FG, alpha=a2,
                fontfamily='sans-serif', linespacing=1.5)

    if t > 0.4:
        arrow_alpha = min(1.0, (t-0.4)*5)
        ax.annotate('', xy=(0.5, 0.38), xytext=(0.5, 0.48),
                    arrowprops=dict(arrowstyle='->', color=TEAL, lw=3, alpha=arrow_alpha),
                    transform=ax.transAxes)

# ── Scene 15 : End card (4 s) ─────────────────────────────────────────────
def scene_end(f):
    clear()
    ax = ax_dark()
    t = f / (FPS * 4)
    a = min(1.0, t * 3)

    ax.text(0.5, 0.68, 'Thank you', transform=ax.transAxes,
            fontsize=40, color=FG, ha='center', fontweight='bold',
            alpha=a, fontfamily='sans-serif')
    ax.text(0.5, 0.52,
            '$\\boldsymbol{Naive\\ Bayes\\ Spam\\ Classifier}$  |  CM12002',
            transform=ax.transAxes, fontsize=14,
            color=BLUE, ha='center', alpha=a)
    ax.text(0.5, 0.39,
            '$\\boldsymbol{89\\%}$ accuracy  |  Bernoulli Naïve Bayes',
            transform=ax.transAxes, fontsize=13,
            color=COMMENT, ha='center', alpha=a)

# ── Render ────────────────────────────────────────────────────────────────
scenes = [
    (scene_title,          3),
    (scene_problem,        5),
    (scene_method_compare, 8),
    (scene_dataset_shape,  6),
    (scene_formula,        7),
    (scene_bernoulli,      8),
    (scene_train1,         5),
    (scene_train2,         5),
    (scene_train3,         7),
    (scene_laplace,        7),
    (scene_absent,         6),
    (scene_predict,        5),
    (scene_results,        7),
    (scene_nn_future,     10),
    (scene_end,            4),
]

OUT = os.path.expanduser('~/Desktop/spamVid3.mp4')

with writer.saving(fig, OUT, dpi=120):
    for scene_fn, duration_s in scenes:
        n_frames = duration_s * FPS
        for f in range(n_frames):
            scene_fn(f)
            writer.grab_frame()

print('Done:', OUT)