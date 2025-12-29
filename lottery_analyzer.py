import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import streamlit as st
from itertools import combinations
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página Streamlit
st.set_page_config(page_title="Análise Loteria - Distribuição Normal", layout="wide")
st.title("🎲 Sistema de Análise Probabilística com Distribuição Normal")

# Funções de carregamento
@st.cache_data
def load_lottery_data(file_path):
    """Carrega jogos da loteria"""
    games = []
    with open(file_path, 'r') as f:
        for line in f:
            numbers = [int(n.strip()) for n in line.strip().split(',')]
            games.append(sorted(numbers))
    return np.array(games)

# Análise de distribuição normal
class NormalDistributionAnalyzer:
    """Analisa padrões usando distribuição normal"""
    
    def __init__(self, games):
        self.games = games
        self.num_range = 60
        self.game_size = 6
        
    def analyze_frequency_distribution(self):
        """Analisa se a frequência dos números segue distribuição normal"""
        frequency = np.zeros(self.num_range + 1)
        
        for game in self.games:
            for num in game:
                frequency[num] += 1
        
        # Remove o zero (índice 0)
        frequency = frequency[1:]
        
        # Testa normalidade com Shapiro-Wilk
        stat, p_value = stats.shapiro(frequency)
        
        # Calcula parâmetros da distribuição normal ajustada
        mu, sigma = norm.fit(frequency)
        
        return {
            'frequency': frequency,
            'mean': mu,
            'std': sigma,
            'shapiro_stat': stat,
            'shapiro_p': p_value,
            'is_normal': p_value > 0.05
        }
    
    def analyze_sum_distribution(self):
        """Analisa a soma dos números em cada jogo"""
        sums = np.array([np.sum(game) for game in self.games])
        
        mu, sigma = norm.fit(sums)
        stat, p_value = stats.shapiro(sums)
        
        return {
            'sums': sums,
            'mean': mu,
            'std': sigma,
            'shapiro_stat': stat,
            'shapiro_p': p_value,
            'is_normal': p_value > 0.05
        }
    
    def analyze_position_distribution(self):
        """Analisa distribuição por posição (1º número, 2º número, etc)"""
        positions = {i: [] for i in range(self.game_size)}
        
        for game in self.games:
            for pos, num in enumerate(game):
                positions[pos].append(num)
        
        position_stats = {}
        for pos, values in positions.items():
            mu, sigma = norm.fit(values)
            stat, p_value = stats.shapiro(values)
            position_stats[pos] = {
                'values': values,
                'mean': mu,
                'std': sigma,
                'is_normal': p_value > 0.05
            }
        
        return position_stats
    
    def analyze_gaps_distribution(self):
        """Analisa distribuição dos gaps entre números consecutivos"""
        all_gaps = []
        
        for game in self.games:
            gaps = [game[i+1] - game[i] for i in range(len(game)-1)]
            all_gaps.extend(gaps)
        
        mu, sigma = norm.fit(all_gaps)
        stat, p_value = stats.shapiro(all_gaps)
        
        return {
            'gaps': np.array(all_gaps),
            'mean': mu,
            'std': sigma,
            'is_normal': p_value > 0.05
        }

# Gerador baseado em distribuição normal
class NormalBasedGenerator:
    """Gera jogos usando insights da distribuição normal"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.freq_dist = analyzer.analyze_frequency_distribution()
        self.sum_dist = analyzer.analyze_sum_distribution()
        self.pos_dist = analyzer.analyze_position_distribution()
        self.gap_dist = analyzer.analyze_gaps_distribution()
    
    def generate_game(self):
        """Gera um jogo respeitando as distribuições normais"""
        # Usa distribuição normal de posições para gerar números
        game = []
        
        for pos in range(6):
            mu = self.pos_dist[pos]['mean']
            sigma = self.pos_dist[pos]['std']
            
            # Gera número dentro da distribuição normal dessa posição
            attempts = 0
            while attempts < 100:
                num = int(np.random.normal(mu, sigma))
                
                # Valida: dentro do range e não repetido
                if 1 <= num <= 60 and num not in game:
                    game.append(num)
                    break
                attempts += 1
            
            # Fallback: se não conseguiu gerar, usa valor médio disponível
            if len(game) <= pos:
                available = [n for n in range(1, 61) if n not in game]
                game.append(available[len(available)//2])
        
        game = sorted(game)
        
        # Verifica se a soma está dentro de 1.5 sigma da média
        game_sum = sum(game)
        target_mean = self.sum_dist['mean']
        target_std = self.sum_dist['std']
        
        # Ajusta se necessário
        if abs(game_sum - target_mean) > 1.5 * target_std:
            return self.generate_game()  # Tenta novamente
        
        return game
    
    def generate_batch(self, n=100):
        """Gera lote de jogos"""
        return [self.generate_game() for _ in range(n)]

# Avaliador de jogos
def evaluate_game(candidate, real_games):
    """Avalia um jogo contra histórico"""
    candidate_set = set(candidate)
    matches = []
    
    for game in real_games:
        match_count = len(candidate_set & set(game))
        matches.append(match_count)
    
    return {
        'avg_matches': np.mean(matches),
        'max_matches': max(matches),
        'min_matches': min(matches),
        'std_matches': np.std(matches),
        'matches_distribution': matches
    }

# Interface Streamlit
st.sidebar.header("⚙️ Configurações")

# Upload de arquivos
training_file = st.sidebar.file_uploader("Upload training_data.csv", type=['csv', 'txt'])
evaluation_file = st.sidebar.file_uploader("Upload evaluation_data.csv", type=['csv', 'txt'])

if training_file and evaluation_file:
    # Salva temporariamente
    with open("training_data.csv", "wb") as f:
        f.write(training_file.getvalue())
    with open("evaluation_data.csv", "wb") as f:
        f.write(evaluation_file.getvalue())
    
    # Carrega dados
    training_games = load_lottery_data("training_data.csv")
    evaluation_games = load_lottery_data("evaluation_data.csv")
    
    st.success(f"✅ Dados carregados: {len(training_games)} jogos de treino, {len(evaluation_games)} jogos de avaliação")
    
    # Análise de distribuição normal
    st.header("📊 Análise de Distribuição Normal")
    
    analyzer = NormalDistributionAnalyzer(training_games)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição de Frequência")
        freq_analysis = analyzer.analyze_frequency_distribution()
        
        fig = go.Figure()
        
        # Histograma de frequência
        fig.add_trace(go.Bar(
            x=list(range(1, 61)),
            y=freq_analysis['frequency'],
            name='Frequência Real',
            marker_color='lightblue'
        ))
        
        # Curva normal teórica
        x = np.linspace(1, 60, 100)
        y = norm.pdf(x, freq_analysis['mean'], freq_analysis['std']) * len(training_games) * 6
        fig.add_trace(go.Scatter(
            x=x, y=y,
            name='Distribuição Normal Teórica',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title=f"Frequência dos Números (μ={freq_analysis['mean']:.1f}, σ={freq_analysis['std']:.1f})",
            xaxis_title="Número",
            yaxis_title="Frequência"
        )
        st.plotly_chart(fig, width='stretch')
        
        is_normal = "✅ SIM" if freq_analysis['is_normal'] else "❌ NÃO"
        st.metric("Segue Distribuição Normal?", is_normal, 
                 f"p-value: {freq_analysis['shapiro_p']:.4f}")
    
    with col2:
        st.subheader("Distribuição de Somas")
        sum_analysis = analyzer.analyze_sum_distribution()
        
        fig = go.Figure()
        
        # Histograma de somas
        fig.add_trace(go.Histogram(
            x=sum_analysis['sums'],
            name='Somas Reais',
            nbinsx=30,
            marker_color='lightgreen',
            opacity=0.7
        ))
        
        # Curva normal
        x = np.linspace(min(sum_analysis['sums']), max(sum_analysis['sums']), 100)
        y = norm.pdf(x, sum_analysis['mean'], sum_analysis['std']) * len(sum_analysis['sums']) * 10
        fig.add_trace(go.Scatter(
            x=x, y=y,
            name='Distribuição Normal',
            line=dict(color='darkgreen', width=2)
        ))
        
        fig.update_layout(
            title=f"Soma dos Números (μ={sum_analysis['mean']:.1f}, σ={sum_analysis['std']:.1f})",
            xaxis_title="Soma",
            yaxis_title="Frequência"
        )
        st.plotly_chart(fig, width='stretch')
        
        is_normal = "✅ SIM" if sum_analysis['is_normal'] else "❌ NÃO"
        st.metric("Segue Distribuição Normal?", is_normal)
    
    # Distribuição por posição
    st.subheader("Distribuição por Posição no Jogo")
    pos_analysis = analyzer.analyze_position_distribution()
    
    fig = go.Figure()
    
    for pos in range(6):
        fig.add_trace(go.Violin(
            y=pos_analysis[pos]['values'],
            name=f'{pos+1}º número',
            box_visible=True,
            meanline_visible=True
        ))
    
    fig.update_layout(
        title="Distribuição de Valores por Posição",
        yaxis_title="Valor do Número",
        xaxis_title="Posição no Jogo"
    )
    st.plotly_chart(fig, width='stretch')
    
    # Gerador de jogos
    st.header("🎯 Gerador Baseado em Distribuição Normal")
    
    num_candidates = st.slider("Número de candidatos a gerar", 10, 1000, 100)
    
    if st.button("🚀 Gerar e Avaliar Candidatos"):
        with st.spinner("Gerando candidatos..."):
            generator = NormalBasedGenerator(analyzer)
            candidates = generator.generate_batch(num_candidates)
            
            # Avalia candidatos
            results = []
            for candidate in candidates:
                eval_train = evaluate_game(candidate, training_games)
                eval_eval = evaluate_game(candidate, evaluation_games)
                
                results.append({
                    'game': candidate,
                    'avg_train': eval_train['avg_matches'],
                    'max_train': eval_train['max_matches'],
                    'avg_eval': eval_eval['avg_matches'],
                    'max_eval': eval_eval['max_matches'],
                    'combined': (eval_train['avg_matches'] + eval_eval['avg_matches']) / 2
                })
            
            results.sort(key=lambda x: x['combined'], reverse=True)
            
            st.success("✅ Candidatos gerados e avaliados!")
            
            # Mostra top 10
            st.subheader("🏆 Top 10 Melhores Jogos")
            
            for i, result in enumerate(results[:10], 1):
                with st.expander(f"#{i}: {','.join(map(str, result['game']))} (Score: {result['combined']:.2f})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Média Treino", f"{result['avg_train']:.2f}")
                        st.metric("Máximo Treino", result['max_train'])
                    with col2:
                        st.metric("Média Avaliação", f"{result['avg_eval']:.2f}")
                        st.metric("Máximo Avaliação", result['max_eval'])
                    with col3:
                        st.metric("Score Combinado", f"{result['combined']:.2f}")
    
    # Teste de jogo personalizado
    st.header("🎮 Teste Seu Jogo")
    
    st.write("Insira um jogo para avaliar (6 números de 1 a 60, separados por vírgula)")
    user_input = st.text_input("Exemplo: 5,12,23,34,45,56", "")
    
    if user_input:
        try:
            user_game = [int(n.strip()) for n in user_input.split(',')]
            
            if len(user_game) == 6 and all(1 <= n <= 60 for n in user_game):
                user_game = sorted(user_game)
                
                # Avalia jogo do usuário
                eval_train = evaluate_game(user_game, training_games)
                eval_eval = evaluate_game(user_game, evaluation_games)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📈 Performance vs Treino")
                    st.metric("Média de Acertos", f"{eval_train['avg_matches']:.2f}")
                    st.metric("Máximo de Acertos", eval_train['max_matches'])
                    st.metric("Mínimo de Acertos", eval_train['min_matches'])
                    
                    # Histograma de matches
                    fig = px.histogram(
                        x=eval_train['matches_distribution'],
                        nbins=7,
                        title="Distribuição de Acertos (Treino)"
                    )
                    fig.update_layout(xaxis_title="Números Acertados", yaxis_title="Frequência")
                    st.plotly_chart(fig, width='stretch')
                
                with col2:
                    st.subheader("📈 Performance vs Avaliação")
                    st.metric("Média de Acertos", f"{eval_eval['avg_matches']:.2f}")
                    st.metric("Máximo de Acertos", eval_eval['max_matches'])
                    st.metric("Mínimo de Acertos", eval_eval['min_matches'])
                    
                    fig = px.histogram(
                        x=eval_eval['matches_distribution'],
                        nbins=7,
                        title="Distribuição de Acertos (Avaliação)"
                    )
                    fig.update_layout(xaxis_title="Números Acertados", yaxis_title="Frequência")
                    st.plotly_chart(fig, width='stretch')
                
                # Análise estatística do jogo
                st.subheader("🔬 Análise Estatística do Seu Jogo")
                
                game_sum = sum(user_game)
                sum_mean = sum_analysis['mean']
                sum_std = sum_analysis['std']
                z_score = (game_sum - sum_mean) / sum_std
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Soma", game_sum)
                with col2:
                    st.metric("Z-Score", f"{z_score:.2f}")
                with col3:
                    percentile = stats.norm.cdf(z_score) * 100
                    st.metric("Percentil", f"{percentile:.1f}%")
                
                if abs(z_score) <= 1:
                    st.success("✅ Seu jogo está dentro de 1 desvio padrão da média (68% dos jogos)")
                elif abs(z_score) <= 2:
                    st.warning("⚠️ Seu jogo está entre 1 e 2 desvios padrão (95% dos jogos)")
                else:
                    st.error("❌ Seu jogo é estatisticamente atípico (fora de 2 desvios padrão)")
                
            else:
                st.error("❌ Jogo inválido. Insira exatamente 6 números entre 1 e 60.")
        except:
            st.error("❌ Formato inválido. Use: número,número,número,...")

else:
    st.info("👈 Faça upload dos arquivos training_data.csv e evaluation_data.csv na barra lateral para começar")
    
    st.markdown("""
    ### 📚 Sobre este Sistema
    
    Este sistema usa **Distribuição Normal** (Gaussiana) para:
    
    1. **Análise de Padrões**: Identifica se os dados seguem distribuição normal
    2. **Geração Inteligente**: Cria jogos respeitando as distribuições observadas
    3. **Avaliação Estatística**: Compara jogos usando Z-score e percentis
    
    #### Por que Distribuição Normal?
    
    Em processos aleatórios **verdadeiramente equiprováveis** (como sorteios de loteria):
    - Frequências de números tendem à uniformidade
    - Somas convergem para distribuição normal (Teorema Central do Limite)
    - Gaps entre números seguem padrões previsíveis
    
    ⚠️ **Importante**: Mesmo usando estatística, loteria permanece **aleatória**.
    Este sistema identifica padrões históricos, não prevê o futuro.
    """)
