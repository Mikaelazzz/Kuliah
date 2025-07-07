# FSA
# None

# Sentiment Analysis
# None

# Visualize Vectorize
# !pip install --force-reinstall numpy==1.26.4 scipy==1.11.4 scikit-learn==1.6.1 gensim==4.3.2 matplotlib==3.8.4


# Model Transformer
# None


# FSA
# None

# Sentiment Analysis
from collections import Counter
import math

# Visualize Vectorize
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Model Transformer
from transformers import pipeline

# FSA
def state_date(inputUser):
  state = 0

  for char in inputUser:
      if state == 0:
          if char.isdigit():
              state = 1  # q1
          else:
              return False
      elif state == 1:
          if char.isdigit():
              state = 2  # q2
          else:
              return False
      elif state == 2:
          if char == '/':
              state = 3  # q3
          else:
              return False
      elif state == 3:
          if char.isdigit():
              state = 4  # q4
          else:
              return False
      elif state == 4:
          if char.isdigit():
              state = 5  # q5
          else:
              return False
      elif state == 5:
          if char == '/':
              state = 6  # q6
          else:
              return False
      elif state == 6:
          if char.isdigit():
              state = 7  # q7
          else:
              return False
      elif state == 7:
          if char.isdigit():
              state = 8  # q8
          else:
              return False
      elif state == 8:
          if char.isdigit():
              state = 9  # q9
          else:
              return False
      elif state == 9:
          if char.isdigit():
              state = 10  # q10
          else:
              return False
      else:
          return False  # Jika input tidak valid

  return state == 10 # jika state sudah 10 (sesuai dengan format date)

tanggal1 = state_date("12/06/2025")
print(bool(tanggal1))

tanggal2 = state_date("12/06/202")
print(bool(tanggal2))

user_input = input("Masukkan tanggal (format DD/MM/YYYY): ")

if state_date(user_input):
    print("Format tanggal valid")
else:
    print("Format tanggal tidak valid")


# Sentiment Analysis

# Dataset latih
data = [
    ("saya suka film ini", "positif"),
    ("filmnya sangat buruk", "negatif"),
    ("aktor luar biasa", "positif"),
    ("cerita tidak menarik", "negatif"),
    ("bagus dan menyenangkan", "positif"),
    ("tidak suka dengan akhir ceritanya", "negatif"),
    ("pengalaman menonton yang buruk", "negatif"),
    ("benar-benar bagus dan menghibur", "positif"),
    ("membosankan dan mengecewakan", "negatif"),
    ("akting yang brilian", "positif")
]

# Tokenisasi dan pemisahan label
docs = [(text.lower().split(), label) for text, label in data]

# Hitung jumlah dokumen per kelas
class_counts = Counter(label for _, label in docs)

# Hitung frekuensi kata per kelas
word_counts = {"positif": Counter(), "negatif": Counter()}
for words, label in docs:
    word_counts[label].update(words)

# Total vokabuler unik
vocab = set()
for words, _ in docs:
    vocab.update(words)
V = len(vocab)  # Jumlah vokabuler

# Total kata per kelas
total_words = {
    "positif": sum(word_counts["positif"].values()),
    "negatif": sum(word_counts["negatif"].values())
}

# Fungsi untuk menghitung likelihood dengan Laplace smoothing
def p_word_given_class(word, class_label):
    return (word_counts[class_label][word] + 1) / (total_words[class_label] + V)

# Fungsi untuk menghitung log probabilitas posterior
def predict(sentence):
    tokens = sentence.lower().split()
    log_prob = {}
    for c in class_counts:
        prior = math.log(class_counts[c] / len(docs))
        likelihood = sum(math.log(p_word_given_class(w, c)) for w in tokens)
        log_prob[c] = prior + likelihood
    return max(log_prob, key=log_prob.get)

# Prediksi kalimat uji
test_sentence = "saya sangat tidak suka"
predicted_sentiment = predict(test_sentence)

print(f"Kalimat: '{test_sentence}'")
print(f"Prediksi Sentimen: {predicted_sentiment.capitalize()}")



# Visualize Vectorize

# Dataset (masih sederhana tapi cukup untuk contoh)
sentences = [
    # Binatang & Peliharaan
    ["cat", "dog", "animal", "pet", "bark", "meow", "fur", "tail", "paws", "cute"],
    ["lion", "tiger", "wild", "zoo", "roar", "predator", "hunter", "animal", "nature", "jungle"],

    # Pemrograman & Teknologi
    ["python", "java", "code", "programming", "algorithm", "function", "variable", "loop", "compile", "debug"],
    ["developer", "software", "engineer", "frontend", "backend", "react", "node", "github", "code", "deploy"],
    ["machine", "learning", "model", "neural", "network", "data", "ai", "training", "deep", "tensor"],

    # Waktu & Kalender
    ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "weekend", "weekday", "calendar"],
]

# Latih model Word2Vec
model = Word2Vec(sentences, vector_size=50, window=3, min_count=1, sg=1, epochs=500, seed=42)

# Ambil semua kata dan vektornya
words = list(model.wv.index_to_key)
word_vectors = [model.wv[word] for word in words]

# Langsung PCA tanpa scaling
pca = PCA(n_components=2)
result = pca.fit_transform(word_vectors)

# Visualisasi
plt.figure(figsize=(12, 8))
plt.scatter(result[:, 0], result[:, 1], alpha=0.6)
for i, word in enumerate(words):
    plt.annotate(word, xy=(result[i, 0], result[i, 1]), xytext=(5, 2),
                 textcoords='offset points', ha='right', va='bottom')
plt.title("Word2Vec Visualization (PCA, No Scaling)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.grid(True)
plt.show()


# Model Transformer

unmasker = pipeline('fill-mask', model='distilbert-base-uncased')
unmasker("Hello I'm a [MASK] model.")

from transformers import DistilBertTokenizer, DistilBertModel
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)

from transformers import DistilBertTokenizer, TFDistilBertModel
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = TFDistilBertModel.from_pretrained("distilbert-base-uncased")
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='tf')
output = model(encoded_input)

from transformers import pipeline
unmasker = pipeline('fill-mask', model='distilbert-base-uncased')
unmasker("The White man worked as a [MASK].")


unmasker("The Black woman worked as a [MASK].")
