import random
from itertools import combinations

def correct_form(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        try:
            n = int(lines[0].strip())
        except ValueError:
            return False
        
        # n lignes après la première
        if len(lines[1:]) != n:
            return False
        
        # Vérifier le format des n lignes restantes
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 3:
                return False
            
            # H ou V
            if parts[0] not in {'H', 'V'}:
                return False
            
            # ensuite un int
            try:
                m = int(parts[1])
            except ValueError:
                return False
            
            # m mots après le int
            if len(parts[2:]) != m:
                return False
        
        return True  # valide
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return False

fichier = "test1.txt"
if correct_form(fichier):
    print("Le fichier est valide.")
else:
    print("Le fichier est invalide.")

    
from collections import Counter

def scoring(file_path):
    if correct_form(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Liste pour stocker les mots avec les doublons
        word_lists = []
        i = 1  # Commencer après la première ligne (nombre total)

        while i < len(lines):
            parts = lines[i].strip().split()
            line_type = parts[0]
            words = parts[2:]  # Extraire les mots

            if line_type == 'H':
                # Ajouter les mots directement pour les lignes H
                word_lists.append(words)  # Liste pour conserver les doublons
                i += 1
            elif line_type == 'V':
                # Regrouper deux lignes V consécutives
                current_list = words[:]
                if i + 1 < len(lines) and lines[i + 1].startswith('V'):
                    next_parts = lines[i + 1].strip().split()
                    next_words = next_parts[2:]
                    current_list.extend(next_words)  # Conserver les doublons
                    i += 1  # Sauter la deuxième ligne V
                word_lists.append(current_list)
                i += 1

        # calcul du score total
        #print(word_lists)
        score_total = 0
        for j in range(len(word_lists) - 1):
            #convertir en Counter pour gérer les doublons
            counter1 = Counter(word_lists[j])
            counter2 = Counter(word_lists[j + 1])

            #calcul des intersections et des différences
            communs = sum((counter1 & counter2).values())  # Intersection
            unique1 = sum((counter1 - counter2).values())  # Uniques dans set1
            unique2 = sum((counter2 - counter1).values())  # Uniques dans set2

            #Score entre deux ensembles
            score_ligne = min(communs, unique1, unique2)
            score_total += score_ligne

        return score_total

    else:
        return "Fichier d'entrée pas de la bonne forme"

    


    
def ecrire_fichier_sortie(file_path, lignes):
    try:
        with open(file_path, 'w') as file:
            for line in lignes:
                file.write(f"{line.strip()}\n")
        print(f"Fichier écrit avec succès : {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier : {e}")

    

def greedy_generation_optimise(file_path):
    def calculate_score(line1, line2):
        """Calcule le score entre deux lignes (H ou V)."""
        if isinstance(line1, tuple):  # si la ligne est une combinaison de deux V
            words1 = line1[2] 
        else:
            words1 = set(line1.split()[2:])  # extraction des mots pour une ligne simple

        if isinstance(line2, tuple):  # idem pour la deuxième ligne
            words2 = line2[2]
        else:
            words2 = set(line2.split()[2:])

        communs = len(words1 & words2)
        unique1 = len(words1 - words2)
        unique2 = len(words2 - words1)
        return min(communs, unique1, unique2)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # extraction des lignes et vérification du format
    first_line = lines[0].strip()
    remaining_lines = [line.strip() for line in lines[1:]]
    v_lines = [line for line in remaining_lines if line.startswith('V')]
    h_lines = [line for line in remaining_lines if line.startswith('H')]

    # préparer les combinaisons des lignes verticales
    v_combinations = []
    used_v = set()  # pour éviter de doubler les lignes V
    for i, v1 in enumerate(v_lines):            
        # sélectionner jusqu'à 2 combinaisons aléatoires avec d'autres lignes
        potential_pairs = [(v1, v2) for j, v2 in enumerate(v_lines) if i < j]
        if len(potential_pairs) > 2:    #choisir nbr
            potential_pairs = random.sample(potential_pairs, 2)  # prendre au hasard 2 paires pour chaque V
        for v1, v2 in potential_pairs:
            if v1 not in used_v and v2 not in used_v:  # éviter de réutiliser les mêmes lignes V
                v_combinations.append((v1, v2, set(v1.split()[2:]) | set(v2.split()[2:])))
                used_v.add(v1)
                used_v.add(v2)

    # exclure les lignes V déjà utilisées dans les combinaisons
    unused_v_lines = [v for v in v_lines if v not in used_v]

    # initialisation de l'approche gloutonne
    all_lines = h_lines + unused_v_lines + v_combinations  # H + V restants + combinaisons (V, V, union_tags)
    current_line = all_lines.pop(0)
    ordered_lines = [current_line]

    test=0
    while all_lines:
        test = test+1
        if test == 9000:
            print("10 pourcent des calcules sont faites")
        best_score = -1
        best_line = None
        best_index = -1

        for index, line in enumerate(all_lines[:700]):
            score = calculate_score(current_line, line)
            if score > best_score:
                best_score = score
                best_line = line
                best_index = index

        # Ajouter la meilleure ligne trouvée
        current_line = best_line
        ordered_lines.append(current_line)
        all_lines.pop(best_index)

    # Reconstruction des lignes finales
    final_lines = []
    
    for line in ordered_lines:
        
        if isinstance(line, tuple):  # Ligne composée (deux V)
            v1, v2, _ = line
            final_lines.append(v1)
            final_lines.append(v2)
        else:
            final_lines.append(line)

    return [first_line] + final_lines






    
resultat = greedy_generation_optimise('./instances/d_pet_pictures.txt')
print(resultat)
ecrire_fichier_sortie("res2.txt", resultat)
print(scoring("res2.txt"))

