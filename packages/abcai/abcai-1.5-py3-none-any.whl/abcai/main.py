def list():
    lists = [
        "alpha_beta_pruning.py",
        "A_star.py",
        "BFS(breath).py",
        "cryto_arthrmatic.py",
        "DFS(depth).py",
        "expert_system.py",
        "min_max.py",
        "Naive_Bayes.py",
        "NLP_token.py",
        "predicate-logic.py",
        "sematic_net.py",
        "spell_check.py",
    ]
    for num, i in enumerate(lists):
        print(num + 1, i)


def run():
    ch = int(input("Enter the number !!!🔎"))
    if ch == 1:
        # with open("./Programs/BFS(breath).py", "r") as info:
        #     con = info.read()

        #     print(con)
        # with open("1.py", "w") as file:
        #     file.write(con)

        def show():
            """
            def bfs(graph, start):
                visited = set()
                queue = []
                visited.add(start)
                queue.append(start)

                while queue:
                    node = queue.pop(0)
                    print(node, end="-->")

                    for neigh in graph[node]:
                        if neigh not in visited:
                            visited.add(neigh)
                            queue.append(neigh)


            if __name__ == "__main__":
                graph = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}

                print("BFS starting from 2")
                bfs(graph, 2)
            """

        show()
        print(show.__doc__)
    if ch == 2:

        def show():
            """
            import heapq

            # Define a grid (0 represents empty, 1 represents obstacles)
            grid = [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 1],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ]

            # Define the start and goal positions
            start = (0, 0)
            goal = (4, 4)


            # Define a heuristic function (Manhattan distance)
            def heuristic(node, goal):
                return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


            # A* algorithm
            def astar(grid, start, goal):
                open_list = [(0.0, start)]  # Priority queue (f-score, node)
                came_from = {}  # Dictionary to store the parent node of each node

                # Initialize g_score with all nodes set to infinity
                g_score = {
                    (x, y): float("inf") for x in range(len(grid)) for y in range(len(grid[0]))
                }
                g_score[start] = 0

                f_score = {node: float("inf") for node in g_score}
                f_score[start] = heuristic(start, goal)

                while open_list:
                    _, current = heapq.heappop(open_list)

                    if current == goal:
                        path = []
                        while current in came_from:
                            path.append(current)
                            current = came_from[current]
                        return path[::-1]

                    for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        x, y = current[0] + neighbor[0], current[1] + neighbor[1]

                        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0:
                            tentative_g_score = g_score[current] + 1

                            if tentative_g_score < g_score[(x, y)]:
                                came_from[(x, y)] = current
                                g_score[(x, y)] = tentative_g_score
                                f_score[(x, y)] = tentative_g_score + heuristic((x, y), goal)
                                heapq.heappush(open_list, (f_score[(x, y)], (x, y)))

                return None  # No path found


            # Find the path
            path = astar(grid, start, goal)

            if path:
                print("Path found:")
                for node in path:
                    print(node)
            else:
                print("No path found.")
            """

        show()
        print(show.__doc__)
    if ch == 3:

        def show():
            """def dfs(graph, start, visited):
                # Check if the 'start' vertex has not been visited.
                if start not in visited:
                    # Print the current 'start' vertex as part of the traversal.
                    print(start, end=" ")
                    # Mark the 'start' vertex as visited by adding it to the 'visited' set.
                    visited.add(start)
                    # Explore neighbors of the current 'start' vertex using recursion.
                    for neighbor in graph[start]:
                        dfs(graph, neighbor, visited)


            # Example usage:
            if __name__ == "__main__":
                # Define a sample graph as an adjacency list where letters represent vertices.
                graph = {
                    "A": ["B", "C"],
                    "B": ["A", "D", "E"],
                    "C": ["A", "F"],
                    "D": ["B"],
                    "E": ["B", "F"],
                    "F": ["C", "E"],
                }

                # Create an empty set 'visited' to keep track of visited vertices during DFS.
                visited = set()

                # Print a message indicating the start of the DFS traversal.
                print("Depth-First Traversal (starting from vertex 'A'):")

                # Call the 'dfs' function with the sample graph, starting vertex 'A', and the 'visited' set.
                dfs(graph, "A", visited)"""

        show()
        print(show.__doc__)

    if ch == 4:

        def show():
            """
            class TreeNode:
                def __init__(self, score):
                    self.score = score
                    self.children = []


            # Build a tree with scores at each node
            root = TreeNode(2)
            root.children = [TreeNode(7), TreeNode(5), TreeNode(4)]

            root.children[0].children = [TreeNode(3), TreeNode(8), TreeNode(3)]
            root.children[1].children = [TreeNode(1), TreeNode(2), TreeNode(6)]
            root.children[2].children = [TreeNode(2), TreeNode(4), TreeNode(7)]


            # Define the alpha-beta pruning function
            def alpha_beta(node, depth, alpha, beta, is_maximizing):
                if depth == 0 or not node.children:
                    return node.score

                if is_maximizing:
                    max_eval = float("-inf")
                    for child in node.children:
                        eval = alpha_beta(child, depth - 1, alpha, beta, False)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                    return max_eval
                else:
                    min_eval = float("inf")
                    for child in node.children:
                        eval = alpha_beta(child, depth - 1, alpha, beta, True)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
                    return min_eval


            if __name__ == "__main__":
                result = alpha_beta(root, 3, float("-inf"), float("inf"), True)
                print("Optimal value:", result)
            """

        show()
        print(show.__doc__)

    if ch == 5:

        def show():
            """
            from itertools import permutations


            def solve_cryptarithmetic(puzzle):
                letters = set("".join(puzzle))
                print(letters)
                if len(letters) > 10:
                    return "Too many letters for unique digit assignment."

                for perm in permutations(range(10), len(letters)):
                    if all(perm[puzzle[i].index(puzzle[i][0])] != 0 for i in range(len(puzzle))):
                        mapping = dict(zip(letters, perm))
                        num1 = int("".join([str(mapping[c]) for c in puzzle[0]]))
                        num2 = int("".join([str(mapping[c]) for c in puzzle[1]]))
                        num3 = int("".join([str(mapping[c]) for c in puzzle[2]]))

                        if num1 + num2 == num3:
                            return mapping

                return "No solution found."


            def main():
                print("Example : \n First word + Second word = Third word")
                a = input("ENter the first word = ")
                b = input("ENter the second word = ")
                c = input("ENter the third word = ")
                puzzle = [a, b, c]
                solution = solve_cryptarithmetic(puzzle)
                print(solution)


            main()"""

        show()
        print(show.__doc__)

    if ch == 6:

        def show():
            """
            import pandas as pd


            class MedicalExpertSystem:
                def __init__(self):

                    self.__symptoms = []
                    self.__diagnosis = None
                    self.__patient_data = pd.DataFrame(columns=["Symptoms", "Diagnosis"])

                def __ask_question(self, question):

                    answer = input(question + " (yes/no): ").strip().lower()
                    if answer == "yes":
                        return True
                    elif answer == "no":
                        return False
                    else:
                        print("Invalid input. Please answer with 'yes' or 'no'.")
                        return self.__ask_question(question)

                def __diagnose(self):

                    if self.__ask_question("Do you have a fever?"):
                        self.__symptoms.append("fever")
                    if self.__ask_question("Do you have a headache?"):
                        self.__symptoms.append("headache")
                    if self.__ask_question("Do you have a cough?"):
                        self.__symptoms.append("cough")

                    new_data = pd.DataFrame(
                        {"Symptoms": [", ".join(self.__symptoms)], "Diagnosis": [""]}
                    )
                    self.__patient_data = pd.concat(
                        [self.__patient_data, new_data], ignore_index=True
                    )

                    if "fever" in self.__symptoms and "headache" in self.__symptoms:
                        self.__diagnosis = "You might have the flu."
                    elif "fever" in self.__symptoms and "cough" in self.__symptoms:
                        self.__diagnosis = "You might have a cold."
                    else:
                        self.__diagnosis = "Your condition is unclear. Please consult a doctor."

                    self.__patient_data.loc[
                        self.__patient_data.index[-1], "Diagnosis"
                    ] = self.__diagnosis

                def run(self):

                    print("Welcome to the Medical Expert System.")
                    self.__diagnose()
                    print("Diagnosis:", self.__diagnosis)
                    print("Patient Data:")
                    print(self.__patient_data)


            if __name__ == "__main__":
                expert_system = MedicalExpertSystem()
                expert_system.run()
            """

    if ch == 7:

        def show():
            """
            # Tic-Tac-Toe Board
            board = [" " for _ in range(9)]


            # Function to print the board
            def print_board():
                print(f"{board[0]} | {board[1]} | {board[2]}")
                print("---------")
                print(f"{board[3]} | {board[4]} | {board[5]}")
                print("---------")
                print(f"{board[6]} | {board[7]} | {board[8]}")


            # Function to check if the board is full
            def is_full(board):
                return " " not in board


            # Function to check if a player has won
            def is_winner(board, player):
                # Check rows
                for i in range(0, 9, 3):
                    if board[i] == board[i + 1] == board[i + 2] == player:
                        return True
                # Check columns
                for i in range(3):
                    if board[i] == board[i + 3] == board[i + 6] == player:
                        return True
                # Check diagonals
                if board[0] == board[4] == board[8] == player:
                    return True
                if board[2] == board[4] == board[6] == player:
                    return True
                return False


            # Min-Max algorithm
            def minimax(board, depth, is_maximizing):
                scores = {
                    "X": 1,
                    "O": -1,
                    "Tie": 0,
                }

                if is_winner(board, "X"):
                    return scores["X"] - depth
                if is_winner(board, "O"):
                    return scores["O"] + depth
                if is_full(board):
                    return scores["Tie"]

                if is_maximizing:
                    best_score = float("-inf")
                    for i in range(9):
                        if board[i] == " ":
                            board[i] = "X"
                            score = minimax(board, depth + 1, False)
                            board[i] = " "
                            best_score = max(score, best_score)
                    return best_score
                else:
                    best_score = float("inf")
                    for i in range(9):
                        if board[i] == " ":
                            board[i] = "O"
                            score = minimax(board, depth + 1, True)
                            board[i] = " "
                            best_score = min(score, best_score)
                    return best_score


            # Function to find the best move
            def find_best_move(board):
                best_move = -1
                best_score = float("-inf")
                for i in range(9):
                    if board[i] == " ":
                        board[i] = "X"
                        score = minimax(board, 0, False)
                        board[i] = " "
                        if score > best_score:
                            best_score = score
                            best_move = i
                return best_move


            # Main game loop
            while True:
                print_board()
                move = int(input("Enter your move (0-8): "))

                if board[move] != " ":
                    print("Invalid move. Try again.")
                    continue

                board[move] = "O"

                if is_winner(board, "O"):
                    print_board()
                    print("You win!")
                    break

                if is_full(board):
                    print_board()
                    print("It's a tie!")
                    break

                best_move = find_best_move(board)
                board[best_move] = "X"

                if is_winner(board, "X"):
                    print_board()
                    print("Computer wins!")
                    break

                if is_full(board):
                    print_board()
                    print("It's a tie!")
                    break"""

        show()
        print(show.__doc__)

    if ch == 8:

        def show():
            """
            import re
            import numpy as np

            # Sample training data
            data = [
                ("This is a spam email", "spam"),
                ("Buy one get one free", "spam"),
                ("Hello, how are you?", "ham"),
                ("Congratulations, you've won a prize!", "spam"),
                ("Meeting at 3 PM", "ham"),
                ("Get a discount on your next purchase", "spam"),
            ]

            # Preprocess the training data
            word_set = set()
            for text, label in data:
                words = re.findall(r"\'w+", text.lower())
                word_set.update(words)

            word_list = list(word_set)
            word_list.sort()

            # Create a vocabulary
            vocab = {word: index for index, word in enumerate(word_list)}
            # Initialize counts for spam and ham
            spam_count = sum(1 for _, label in data if label == "spam")
            ham_count = sum(1 for _, label in data if label == "ham")


            # Count the occurrences of words in spam and ham messages
            spam_word_count = np.zeros(len(vocab))
            ham_word_count = np.zeros(len(vocab))


            # Populate the counts
            for text, label in data:
                words = re.findall(r"\'w+", text.lower())
                label_count = spam_word_count if label == "spam" else ham_word_count
                for word in words:
                    if word in vocab:
                        word_index = vocab[word]
                        label_count[word_index] += 1


            # Calculate the prior probabilities
            total_messages = len(data)

            prior_spam = spam_count / total_messages
            prior_ham = ham_count / total_messages


            # Input text to classify
            input_text = "You've won a free vacation!"

            # Tokenize and process the input text
            input_words = re.findall(r"\'w+", input_text.lower())

            # Calculate likelihoods and apply the Naive Bayes formula
            likelihood_spam = 1.0
            likelihood_ham = 1.0

            for word in input_words:
                if word in vocab:
                    word_index = vocab[word]

                    likelihood_spam *= (spam_word_count[word_index] + 1) / (spam_count + len(vocab))

                    likelihood_ham *= (ham_word_count[word_index] + 1) / (ham_count + len(vocab))


            # Apply Bayes' theorem
            posterior_spam = (likelihood_spam * prior_spam) / (
                (likelihood_spam * prior_spam) + (likelihood_ham * prior_ham)
            )


            posterior_ham = 1 - posterior_spam

            # Make a classification decision
            if posterior_spam > posterior_ham:
                print("Classified as: Spam")
            else:
                print("Classified as: Ham")"""

        show()
        print(show.__doc__)
    if ch == 9:

        def show():
            """
            import nltk
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from nltk.stem import PorterStemmer

            # Download NLTK resources if not already downloaded
            nltk.download("punkt")
            nltk.download("stopwords")

            # Sample text for processing
            text = "Natural language processing (NLP) is a subfield of artificial intelligence (AI) that deals with the interaction between computers and humans through natural language."

            # Tokenization
            tokens = word_tokenize(text)

            # Stopwords removal
            stop_words = set(stopwords.words("english"))
            filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

            # Stemming
            stemmer = PorterStemmer()
            stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

            # Print the results
            print("Original Text:")
            print(text)

            print("\nTokenized Text:")
            print(tokens)

            print("\nAfter Stopwords Removal:")
            print(filtered_tokens)

            print("\nAfter Stemming:")
            print(stemmed_tokens)"""

        show()
        print(show.__doc__)

    if ch == 10:

        def show():
            """
            class KnowledgeBase:
                def __init__(self):
                    self.facts = set()

                def add_fact(self, fact):
                    self.facts.add(fact)

                def remove_fact(self, fact):
                    self.facts.discard(fact)

                def check_fact(self, fact):
                    return fact in self.facts

                def display_facts(self):
                    print("Facts in the Knowledge Base:")
                    for fact in self.facts:
                        print(fact)

                def to_first_order_logic(self):
                    first_order_logic_facts = []

                    for fact in self.facts:
                        # Split the fact into words
                        words = fact.split()

                        # Check if the fact has the format: [subject] [is/are] [object(s)]
                        if len(words) >= 3 and words[1] in ["is", "are"]:
                            subject = words[0]
                            predicate = words[2]
                            objects = words[3:]

                            # Create a first-order logic statement
                            if len(objects) == 1:
                                first_order_logic = f"{predicate}({subject} {objects[0]})"
                            else:
                                first_order_logic = f"{predicate}({subject} " + " ".join(objects) + ")"

                            first_order_logic_facts.append(first_order_logic)

                    return first_order_logic_facts

            # Create a knowledge base
            kb = KnowledgeBase()

            # Accept facts from the user
            print("Enter facts (one per line). Type 'q' to quit.")
            while True:
                fact_str = input("Enter a fact: ")
                if fact_str.lower() == 'q':
                    break

                kb.add_fact(fact_str)

            # Check if a fact is in the knowledge base
            check_fact_str = input("Enter a fact to check: ")
            if kb.check_fact(check_fact_str):
                print(f"'{check_fact_str}' is a fact in the knowledge base.")
            else:
                print(f"'{check_fact_str}' is not a fact in the knowledge base.")

            # Display all facts in the knowledge base
            kb.display_facts()

            # Convert facts to first-order logic and display
            first_order_logic_facts = kb.to_first_order_logic()
            print("\nFacts in First-Order Logic:")
            for fact in first_order_logic_facts:
                print(fact)"""

        show()
        print(show.__doc__)

    if ch == 11:

        def show():
            """
            class Node:
                def __init__(self, name):
                    self.name = name
                    self.edges = []

                def add_edge(self, relation, node):
                    self.edges.append((relation, node))

                def __str__(self):
                    return self.name


            class SemanticNetwork:
                def __init__(self):
                    self.nodes = []

                def add_node(self, name):
                    node = Node(name)
                    self.nodes.append(node)
                    return node

                def __str__(self):
                    result = "Semantic Network:\n"
                    for node in self.nodes:
                        result += f"{node} has relations:\n"
                        for relation, related_node in node.edges:
                            result += f"  - {relation}: {related_node}\n"
                    return result


            # Create a semantic network
            semantic_net = SemanticNetwork()

            while True:
                print("1. Add Node")
                print("2. Add Relationship")
                print("3. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    node_name = input("Enter node name: ")
                    semantic_net.add_node(node_name)
                    print(f"Node '{node_name}' added.")
                elif choice == "2":
                    node_name = input("Enter node name: ")
                    relation = input("Enter relation: ")
                    related_node_name = input("Enter related node name: ")

                    # Find the nodes with the specified names
                    node = next((n for n in semantic_net.nodes if n.name == node_name), None)
                    related_node = next(
                        (n for n in semantic_net.nodes if n.name == related_node_name), None
                    )

                    if node and related_node:
                        node.add_edge(relation, related_node)
                        print(
                            f"Relationship added: {node_name} -> {relation} -> {related_node_name}"
                        )
                    else:
                        print("One or both nodes not found.")
                elif choice == "3":
                    break
                else:
                    print("Invalid choice. Please try again.")

            # Display the semantic network
            print(semantic_net)
            """

        show()
        print(show.__doc__)

    if ch == 12:

        def show():
            """
            import nltk
            from nltk.corpus import words

            nltk.download("words")

            # Load the NLTK words corpus as a set
            english_words = set(words.words())


            def spell_check(text):
                # Tokenize the input text
                words_to_check = nltk.word_tokenize(text)

                # Check each word in the text against the NLTK English words corpus
                misspelled_words = [
                    word for word in words_to_check if word.lower() not in english_words
                ]

                return misspelled_words


            # Input from the user
            input_text = input("Enter a sentence for spell checking: ")

            # Perform spell checking
            misspelled_words = spell_check(input_text)

            if len(misspelled_words) > 0:
                print("\nMisspelled words:")
                for word in misspelled_words:
                    print(word)
            else:
                print("\nNo misspelled words found.")"""

        show()
        print(show.__doc__)

    print("Done 🔥")
