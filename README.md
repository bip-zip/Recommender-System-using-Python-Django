# Recommender-System-using-Python
This is a simple django project which has a well-working implementation of recommendation systems(content-based filtering and collaborative filtering) for an e-commerce application using python librabries: NumPy, Pandas, Sklearn

For content-based filtering, cosine_similarity has been used to find angular distance vector between products, which falls under sklearn library.
For collaborative-filtering, matrix factorization method has been used to find co-relation between matrices, which falls under NumPy, sklearn libraries.
It has a login portal from where it can distinguish users and recommends product according to their past histories and ratings.
![image](https://user-images.githubusercontent.com/60959655/136474500-7483a78c-2ca0-4302-b136-a192e6117d71.png)

It does have a clean user interface - everything on one page. 
![image](https://user-images.githubusercontent.com/60959655/136474632-f7ec2097-c24f-4220-ac8a-ea10bcbf37a4.png)
![image](https://user-images.githubusercontent.com/60959655/136474965-69e30a8e-075c-4267-b682-da26b16484ce.png)
![image](https://user-images.githubusercontent.com/60959655/136474689-e4d1f98e-be31-402f-86f9-9905289aacfb.png)

It is a simple application programmed using python + django and has django's default database sqlite. 
It stores user's search history and use it to recommend(content-based) products.
It has a 'Rating' model which stores user-product-rating data to recommend(collaborative) products.
It also recommend products on popularity based filtering which is nothing but the count of products with maximum orders.

--------------------------------------Happy coding!!🍀-----------------------------------------------------
