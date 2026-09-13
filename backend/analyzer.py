import io
import json
import base64

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def get_data_summary(df):
    summary = f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n\n"
    summary += "Columns:\n"
    for col in df.columns:
        summary += f"  - {col} ({df[col].dtype})"
        if df[col].isnull().sum() > 0:
            summary += f" [{df[col].isnull().sum()} missing]"
        summary += "\n"
    summary += f"\nBasic Statistics:\n{df.describe(include='all').to_string()}\n"
    return summary


def generate_charts(df):
    plt.style.use('dark_background')
    colors = ['#7c5cfc', '#5cf0fc', '#fc5c7c', '#5cfc7c', '#fcb45c']
    bg_color = '#1a1a2e'

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    charts = []

    if len(numeric_cols) >= 2:
        n_hist = min(len(numeric_cols), 6)
        rows = (n_hist + 1) // 2
        fig, axes = plt.subplots(rows, 2, figsize=(12, 3.5 * rows))
        fig.patch.set_facecolor(bg_color)
        fig.suptitle('Distribution of Numeric Features', color='white', fontsize=14, fontweight='bold', y=1.02)
        axes = axes.flatten() if n_hist > 2 else [axes] if n_hist == 1 else axes.flatten()

        for i, col in enumerate(numeric_cols[:n_hist]):
            ax = axes[i]
            ax.set_facecolor(bg_color)
            ax.hist(df[col].dropna(), bins=15, color=colors[i % len(colors)], alpha=0.8, edgecolor='none')
            ax.set_title(col, color='white', fontsize=11)
            ax.tick_params(colors='#6b6b80', labelsize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        for j in range(n_hist, len(axes)):
            axes[j].set_visible(False)

        plt.tight_layout()
        charts.append(fig_to_base64(fig))
        plt.close(fig)

    if len(numeric_cols) >= 3:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r',
                    center=0, ax=ax, linewidths=0.5,
                    annot_kws={'size': 9, 'color': 'white'},
                    cbar_kws={'shrink': 0.8})
        ax.set_title('Correlation Matrix', color='white', fontsize=14, fontweight='bold', pad=15)
        ax.tick_params(colors='#6b6b80', labelsize=9)
        plt.tight_layout()
        charts.append(fig_to_base64(fig))
        plt.close(fig)

    if categorical_cols:
        n_cat = min(len(categorical_cols), 4)
        fig, axes = plt.subplots(1, n_cat, figsize=(5 * n_cat, 4))
        fig.patch.set_facecolor(bg_color)
        if n_cat == 1:
            axes = [axes]

        for i, col in enumerate(categorical_cols[:n_cat]):
            ax = axes[i]
            ax.set_facecolor(bg_color)
            counts = df[col].value_counts().head(8)
            bars = ax.barh(counts.index.astype(str), counts.values, color=colors[i % len(colors)], alpha=0.8)
            ax.set_title(col, color='white', fontsize=11)
            ax.tick_params(colors='#6b6b80', labelsize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.invert_yaxis()

        plt.tight_layout()
        charts.append(fig_to_base64(fig))
        plt.close(fig)

    return charts


def compute_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    stats = {}

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        top_corrs = []
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                top_corrs.append({
                    'pair': f"{corr.columns[i]} vs {corr.columns[j]}",
                    'correlation': round(corr.iloc[i, j], 3)
                })
        top_corrs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        stats['top_correlations'] = top_corrs[:5]

    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if categorical_cols and numeric_cols:
        group_stats = {}
        for cat in categorical_cols[:2]:
            for num in numeric_cols[:3]:
                try:
                    grouped = df.groupby(cat)[num].mean().round(2).to_dict()
                    group_stats[f"{num} by {cat}"] = grouped
                except Exception:
                    pass
        stats['group_analysis'] = group_stats

    stats['missing_values'] = df.isnull().sum().to_dict()
    stats['row_count'] = len(df)
    stats['col_count'] = len(df.columns)

    return stats


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=150,
                facecolor='#1a1a2e', edgecolor='none')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()
