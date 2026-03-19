# Analysis Results

**Input Folder:** `data/leongross/organized_contrat_decennale/08e88300-6571-4f04-a141-c65468396b69`
**Files Processed:** 2
**Merged JSON Path:** `data/leongross/organized_contrat_decennale/08e88300-6571-4f04-a141-c65468396b69/merged_documents.json`

---


## Document 1: avenant_contrat_sous_traitance

**Document ID:** leongross_contrat_12bafb85-edbf-4b94-8de3-aab781a5fb9a-0gmknkvMmQ8f6muv0ARE6A-1768849254.pdf
**Type:** avenant_contrat_sous_traitance
**Language:** francais

### Summary

**Objet:**
Avenant N°11 à la commande de travaux en sous-traitance

**Parties Identifiées:**


### Dates Clés

| Événement | Période |
|-----------|---------|
| Signature | 22/09/2025 |
| Debut Travaux | 07/01/2026 |
| Fin Travaux | 08/01/2026 |

### Montants

| Description | Montant |
|-------------|---------|
| Ht Total | 29 025,50 € |
| Retenue Garantie | 0 % |
| Prorata Forfaitise | 0 % |

### Obligations Principales


### Incohérences Internes

#### Incoherence Date

- **ID:** date_execution_travaux
- **Gravité:** ELEVEE
- **Localisation:** section '6 - DÉLAI D'EXECUTION'
- **Description:** La durée d'exécution du chantier est extrêmement courte (07/01/2026 à 08/01/2026), ce qui semble incompatible avec les travaux décrits (dépose, manutention, placo et peinture).
- **Impact Métier:** Risque de non-respect des délais techniques ou de qualité des prestations.
- **Recommandation:** Clarifier la durée réelle de prestation et vérifier la faisabilité technique.

#### Non Conformite

- **ID:** renonciation_recours
- **Gravité:** MOYENNE
- **Localisation:**  Article 'Le sous-traitant renonce à tout recours et réclamations pour les faits antérieurs...'
- **Description:** L'avenant inclut une renonciation à des recours pour les faits antérieurs, ce qui va à l'encontre des bonnes pratiques contractuelles de mise en avant des obligations de l'entrepreneur principal.
- **Impact Métier:** Potentiel déséquilibre contractuel entre les parties.
- **Recommandation:** Réviser la clause pour éviter toute interprétation défavorable.

### Conclusion
L'avenant décrit un projet de sous-traitance de peinture et placo, avec un calendrier très serré et des conditions contractuelles déséquilibrées. Des incohérences dans les dates d’exécution et l’obligation de renonciation aux recours antérieurs sont à signaler.

---


## Document 2: attestation_assurance_decennale

**Document ID:** leongross_decennale_alg-0116319c-5557-41da-9ed9-b503cde1d002.pdf
**Type:** attestation_assurance_decennale
**Language:** francais

### Summary

**Objet:**
Attestation d'assurance Responsabilité Civile Décennale (RC Décennale) pour R2G SAS

**Parties Identifiées:**

- **Assureur:** QBE Europe SA/NV - succursale française
- **Assure:** R2G SAS (RADOUANE CHIKHI)
- **Intermediaire:** SOLLY AZAR SAS

### Dates Clés

| Événement | Période |
|-----------|---------|
| Validite | {'debut': '01/01/2026', 'fin': '31/12/2026'} |
| Date Attestation | 18/12/2025 |
| Date Ouverture Chantier | Non spécifiée |

### Montants

| Description | Montant |
|-------------|---------|
| Cotisation Ttc | 2 948,30 € |
| Franchise | 2 500 € |
| Montant Garantie | 7 500 000 € par sinistre |

### Obligations Principales


### Conclusion
L'attestation couvre les activités du sous-traitant pour la période 2026 (peinture, placo, plomberie, etc.) et respecte les exigences du code civil. Le montant de garantie est conforme aux standards du secteur.

---


## Incohérences Croisées (Cross-Document)

### Assurance

- **Type:** Assurance
- **Gravité:** MOYENNE
- **Documents Concernés:** leongross_contrat_12bafb85-edbf-4b94-8de3-aab781a5fb9a-0gmknkvMmQ8f6muv0ARE6A-1768849254.pdf, leongross_decennale_alg-0116319c-5557-41da-9ed9-b503cde1d002.pdf

**Description:**
Les activités décrites dans l'avenant (peinture et placo) correspondent partiellement à celles couvertes par l'attestation d'assurance décennale. La garantie peinture exclut spécifiquement l'étanchéité des façades, mais inclut la partie 'peinture'. Cependant, l'attestation couvre également des activités non évoquées dans l'avenant (plomberie, électricité, etc.).

**Impact Métier:**
Possibilité de confusion sur le périmètre réel des activités garanties, et risque juridique si des activités non listées dans l'avenant sont exécutées.

**Recommandation:**
Expliciter les activités couvertes dans l'avenant pour correspondre strictement à la couverture d'assurance.


### Date

- **Type:** Date
- **Gravité:** MOYENNE
- **Documents Concernés:** leongross_contrat_12bafb85-edbf-4b94-8de3-aab781a5fb9a-0gmknkvMmQ8f6muv0ARE6A-1768849254.pdf, leongross_decennale_alg-0116319c-5557-41da-9ed9-b503cde1d002.pdf

**Description:**
L'avenant mentionne une date de début des travaux (07/01/2026) et une date de fin (08/01/2026), mais l'attestation d'assurance ne précise pas la date exacte d'ouverture du chantier pour la couverture décennale. Cela peut poser problème pour vérifier que le chantier commence sous la couverture assurantielle valide.

**Impact Métier:**
Risque d'absence de couverture si l'ouverture de chantier n'est pas alignée avec la période d'assurance.

**Recommandation:**
Préciser la date exacte d'ouverture du chantier dans l'avenant et s'assurer de son alignement avec la période de validité de l'assurance.


### Date

- **Type:** Date
- **Gravité:** ELEVEE
- **Documents Concernés:** leongross_contrat_12bafb85-edbf-4b94-8de3-aab781a5fb9a-0gmknkvMmQ8f6muv0ARE6A-1768849254.pdf, leongross_decennale_alg-0116310c-5557-41da-9ed9-b503cde1d002.pdf

**Description:**
La durée d'exécution mentionnée dans l'avenant (07/01/2026 au 08/01/2026) est extrêmement courte et semble incompatible avec la nature des prestations détaillées. Ceci pourrait remettre en cause l'adéquation entre la durée des travaux et la couverture d'assurance décennale, qui couvre une durée de 10 ans.

**Impact Métier:**
Risque que les prestations ne soient pas couvertes correctement par l'assurance RC décennale.

**Recommandation:**
Corriger la durée d'exécution pour refléter les activités réalisées et s'assurer que la couverture d'assurance est adaptée à la réalité des travaux.



## Contrôle Assurance Décennale

**Activité Déclarée:** Dépose, manutention, placo et peinture (mentionné dans l'avenant de contrat)

**Activités Couvertes:** Peinture (4.5), Plâtrerie-Staff-Stuc-Gypserie (4.2), Revêtements de surfaces en matériaux souples (4.6)

**Statut Cohérence:** partiellement_coherent

**Risque Identifié:** moyen


**Analyse Détaillée:**
L'activité déclarée dans l'avenant inclut la peinture et le placo, qui sont couvertes par l'assurance décennale. Cependant, certains éléments comme la 'manutention' et 'dépose' ne sont pas explicitement mentionnés dans la couverture. De plus, l'assurance couvre d'autres activités (plomberie, électricité) non mentionnées dans l'avenant. Cela crée une ambiguïté sur le périmètre des prestations garanties.


**Recommandation:**
Clarifier le périmètre exact des activités couvertes dans le contrat de sous-traitance pour éviter toute ambiguïté et ajuster les activités garanties par l'assurance. Ajouter une mention explicite concernant la couverture des activités de 'manutention' et 'dépose'.


## Score de Cohérence Global

| Métrique | Score |
|----------|-------|
| Note sur 100 | **55/100** |


**Justification:**
Incohérences importantes pour les dates d'exécution et le périmètre d'activités, particulièrement entre l'avenant et l'assurance décennale. Le périmètre d'activités garanties ne correspond pas exactement aux prestations déclarées, et la durée extrêmement courte des travaux soulève des questions sur leur faisabilité technique et juridique.


## Conclusion Globale

L'ensemble des documents présente un risque modéré lié à une incohérence entre les activités déclarées dans l'avenant de contrat et celles couvertes par l'assurance décennale. La courte période d'exécution mentionnée ne correspond pas à la nature des travaux ni à la durée de garantie décennale. Il est recommandé d'apporter des clarifications sur la durée réelle des travaux, les activités à couvrir et de s'assurer que la couverture d'assurance est strictement alignée sur le périmètre contractuel.


---

*Document généré automatiquement à partir de analysis_results.json*