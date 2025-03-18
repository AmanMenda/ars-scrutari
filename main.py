# main.py
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional
import re
from collections import Counter
import matplotlib.pyplot as plt

# ========== Data Classes ==========
@dataclass(frozen=True)
class AnalysisResult:
    content: str

@dataclass(frozen=True)
class SkillTrendsResult(AnalysisResult):
    pass

@dataclass(frozen=True)
class CVFormatResult(AnalysisResult):
    pass

@dataclass(frozen=True)
class PatternsResult(AnalysisResult):
    pass

@dataclass(frozen=True)
class PlatformSuccessResult(AnalysisResult):
    pass

@dataclass(frozen=True)
class ResponseTimeResult(AnalysisResult):
    pass

@dataclass(frozen=True)
class RejectionRateResult(AnalysisResult):
    pass

# ========== Base Analyzer ==========
class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._clean_data()

    def _clean_data(self) -> None:
        self.df['Profil_Recherche'] = self.df['Profil_Recherche'].fillna('')
        self.df['Pays'] = self.df['Pays'].str.strip().fillna('Inconnu')
        self.df['Statut'] = self.df['Statut'].str.strip()

# ========== Concrete Analyzers ==========
class SkillTrendsAnalyzer(DataAnalyzer):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.stop_words = set(['en', 'le', 'la', 'de', 'et', 'à', 'pour', 'dans'])

    def _extract_skills(self, text: str) -> List[str]:
        words = re.findall(r'\b\w{4,}\b', text.lower())
        return [word for word in words if word not in self.stop_words]

    def get_results(self) -> SkillTrendsResult:
        skills_by_country = {}
        for country, group in self.df.groupby('Pays'):
            all_skills = []
            for desc in group['Profil_Recherche']:
                all_skills.extend(self._extract_skills(desc))
            skills_by_country[country] = Counter(all_skills).most_common(5)
        
        report = "Compétences les plus recherchées par pays :\n"
        for country, skills in skills_by_country.items():
            report += f"\n{country}:\n"
            for skill, count in skills:
                report += f"- {skill} ({count} occurrences)\n"
        
        return SkillTrendsResult(report)

class CVFormatAnalyzer(DataAnalyzer):
    def get_results(self) -> CVFormatResult:
        cv_formats = self.df['CV'].apply(
            lambda x: (
                re.search(r'\.([a-zA-Z0-9]+)(?=[/?]|$)', str(x)).group(1).lower() 
                if pd.notna(x) and re.search(r'\.([a-zA-Z0-9]+)(?=[/?]|$)', str(x)) 
                else None
            )
        )
        format_counts = cv_formats.value_counts()
        
        report = "Formats de CV utilisés :\n"
        for fmt, count in format_counts.items():
            report += f"- {fmt}: {count} utilisations\n"
        
        return CVFormatResult(report)

class PatternsAnalyzer(DataAnalyzer):
    def get_results(self) -> PatternsResult:
        all_descriptions = ' '.join(self.df['Profil_Recherche'].str.lower())
        keywords = re.findall(r'\b\w{6,}\b', all_descriptions)
        keyword_counts = Counter(keywords).most_common(10)
        
        report = "Mots-clés récurrents dans les descriptions :\n"
        for word, count in keyword_counts:
            report += f"- {word} ({count} occurrences)\n"
        
        return PatternsResult(report)

class PlatformSuccessAnalyzer(DataAnalyzer):
    def get_results(self) -> PlatformSuccessResult:
        platform_stats = self.df.groupby(['Pays', 'Plateforme'])['Statut'].agg(
            total='count',
            responses=lambda x: x[x != 'Sans réponse'].count()
        ).reset_index()
        
        platform_stats['success_rate'] = (platform_stats['responses'] / platform_stats['total'] * 100).round(1)
        
        report = "Taux de réponse par plateforme et pays :\n"
        for (country, platform), data in platform_stats.groupby(['Pays', 'Plateforme']):
            report += f"\n{country} - {platform}:"
            report += f"\n- Taux de réponse: {data['success_rate'].values[0]}%"
            report += f"\n- Candidatures: {data['total'].values[0]}\n"
        
        return PlatformSuccessResult(report)

class ResponseTimeAnalyzer(DataAnalyzer):
    def get_results(self) -> ResponseTimeResult:
        # Filtrer les candidatures avec réponse
        df_responses = self.df[self.df['Statut'] != 'Sans réponse']
        
        # Calculer la durée de réponse
        df_responses['Duree_Reponse'] = (
            df_responses['Date_Reponse'] - df_responses['Date_Candidature']
        ).dt.days

        # Calculer la moyenne
        avg_days = df_responses['Duree_Reponse'].mean()
        
        report = f"Durée moyenne de réponse : {avg_days:.1f} jours\n"
        report += f"Basé sur {len(df_responses)} réponses reçues"
        
        return ResponseTimeResult(report)

class RejectionRateAnalyzer(DataAnalyzer):
    def get_results(self) -> RejectionRateResult:
        # Compter les réponses
        total_reponses = self.df[self.df['Statut'] != 'Sans réponse'].shape[0]
        refus_count = self.df[self.df['Statut'] == 'Refus'].shape[0]
        
        # Calculer le taux
        taux_refus = (refus_count / total_reponses * 100) if total_reponses > 0 else 0
        
        report = f"Taux de refus global : {taux_refus:.1f}%\n"
        report += f"({refus_count} refus sur {total_reponses} réponses)"
        
        return RejectionRateResult(report)

# ========== Analysis Coordinator ==========
class AnalysisCoordinator:
    def __init__(self, file_path: str):
        self.df = pd.read_csv(file_path)
        self.df['Date_Candidature'] = pd.to_datetime(
            self.df['Date_Candidature'], 
            format='%d %B %Y', 
            errors='coerce'
        )
        self.df['Date_Reponse'] = pd.to_datetime(
            self.df['Date_Reponse'], 
            format='%d %B %Y', 
            errors='coerce'
        )
        
    def execute_analysis(self) -> Dict[str, AnalysisResult]:
        return {
            'skill_trends': SkillTrendsAnalyzer(self.df).get_results(),
            'cv_formats': CVFormatAnalyzer(self.df).get_results(),
            'patterns': PatternsAnalyzer(self.df).get_results(),
            'platform_success': PlatformSuccessAnalyzer(self.df).get_results(),
            'response_time': ResponseTimeAnalyzer(self.df).get_results(),
            'rejection_rate': RejectionRateAnalyzer(self.df).get_results()
        }

# ========== Main Execution ==========
if __name__ == "__main__":
    coordinator = AnalysisCoordinator('Suivi entreprises tech - Feuille 1.csv')
    results = coordinator.execute_analysis()
    
    for name, result in results.items():
        print(f"\n=== {name.replace('_', ' ').title()} ===")
        print(result.content)
        
        # Generate simple plots
        if isinstance(result, SkillTrendsResult):
            # My plotting logic if needed
            pass