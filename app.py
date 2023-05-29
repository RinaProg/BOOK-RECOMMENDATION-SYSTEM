from flask import Flask,render_template, request
import numpy as np
import pandas as pd


popular_df = pd.read_pickle(open('popular.pkl','rb'))
pt = pd.read_pickle(open('pt.pkl','rb'))
books = pd.read_pickle(open('books.pkl','rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    rating =np.array(list(popular_df['Avg_rating'].values))
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Num_rating'].values),
                           rat = np.around(rating, decimals=1),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods =['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:8]

    data = []
    for i in similar_items:
        item = []
        temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

        # print(data)

    return render_template('recommend.html', data=data)
@app.route('/contact')
def contact():

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
