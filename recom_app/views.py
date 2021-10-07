from django.shortcuts import render
from django.views.generic import View
from .models import OrderItems, Product, Category,SearchHistory, Rating
from django.db.models import Q

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

class IndexView(View):

    def join_tuple_string(self,strings_tuple) -> str:
        return ' '.join(strings_tuple)

    def get_feature_products(self):
        product_list=list()
        # product_list = list(Product.objects.values_list('name', 'descrption'))
        for i in Product.objects.all(): 
            item= (i.name, i.descrption, str(Category.objects.get(id=(i.category.id))))
            product_list.append(item)
        print(product_list)
        result = list(map(self.join_tuple_string, product_list))
        print('result: ', result, product_list)
        return result
    


    def get_products_with_id(self):
        feature_product = self.get_feature_products()
        all_products_id = list(Product.objects.values_list('id', flat=True))
        products_with_id = {}
        for index, id in enumerate(all_products_id):
            products_with_id[id] = feature_product[index]
        return products_with_id


    def similar_products(self,product_id):
        all_products = self.get_feature_products()
        all_products_id = list(Product.objects.values_list('id', flat=True))
        cm = CountVectorizer().fit_transform(all_products)
        cs = cosine_similarity(cm)
        product_index = all_products_id.index(product_id)
        unsorted_similar_product = list(enumerate(cs[product_index]))
        sorted_similar_product = sorted(unsorted_similar_product, key=lambda x: x[1], reverse=True)
        similar_products_query_set = []

        for i in sorted_similar_product:
            similar_products_query_set.append(Product.objects.get(id=all_products_id[i[0]]))
            print(i)
        return similar_products_query_set[:5]

    

    def coll(self,product_id):
        from django.db import connection

        query = str(Rating.objects.all().query)
        all_ratings = pd.read_sql_query(query, connection)
        # all_ratings=pd.DataFrame(list(Rating.objects.values('rating','user','product'))) 
        print(all_ratings)
        utility_matrix = all_ratings.pivot_table(values = 'rating',index='user_id', columns = 'product_id', fill_value = 0)
        print(utility_matrix,'----------------------------------')
        A = utility_matrix.T
        print(A,'----------------------------------')
        SVD = TruncatedSVD(n_components = 5)
        decomposed_matrix = SVD.fit_transform(A)
        correaltion_matrix = np.corrcoef(decomposed_matrix)
        print(correaltion_matrix,'corell')
        i = product_id
        item_name = list(A.index)
        print(item_name,'================itemname')
        item_ID = item_name.index(i)
        print(item_ID,'================itemid')
        correlation_item_ID = correaltion_matrix[item_ID]
        print(correlation_item_ID,'================co_itemid')


        recommend = list(A.index[correlation_item_ID>0.50])
        collaborative_products_query_set = []
        i=0
        while i<len(recommend):
            print(i)
            collaborative_products_query_set.append(Product.objects.get(id=recommend[i]))
            i+=1
            
        print(collaborative_products_query_set)
        return collaborative_products_query_set



    def get(self, request, *args):
        results=Product.objects.none()
        
        if request.method == 'GET':
            query=request.GET.get('query')
            if not query == None:
                results=Product.objects.filter(Q(name__icontains=query) | Q(descrption__icontains=query))[:10]
        user=request.user
        search_history=SearchHistory.objects.filter(customer=user).order_by('-id')[:5]
        recent_search=SearchHistory.objects.filter(customer=user).last()
        if recent_search:
            recomProduct=Product.objects.filter(Q(name__icontains=(recent_search.query)) | Q(descrption__icontains=(recent_search.query))| Q(category__category__icontains=(recent_search.query))).last()
            content_based=self.similar_products(recomProduct.id)
        else:
            recomProduct=Product.objects.none()
            content_based=Product.objects.none()
        
        if results.exists() :
            SearchHistory.objects.create(customer=user, query=query.lower())

        previous_order=OrderItems.objects.filter(customer=user).order_by('-id')
        lastPreviousOrder=previous_order.first()
        if lastPreviousOrder:
            collaborative=self.coll((lastPreviousOrder.product.id))
            # content_based=Product.objects.filter(category=(lastPreviousOrder.product.category)).order_by('-id').exclude(id=(lastPreviousOrder.product.id))
        else: 
            # content_based=Product.objects.none()
            collaborative=Product.objects.none()

        from django.db.models import Count
        popularity = OrderItems.objects.values('product').annotate(Count('product')).order_by('-product__count').filter(product__count__gt=0)[:5]
        popular_queryset=[]
        for product in popularity:
            prod=product.get('product')
            popular_queryset.append(Product.objects.get(id=prod))
        print(popular_queryset)
        context={
            'previous_order':previous_order,
            'results':results,
            'search_history':search_history,
            'query':query,
            'content_based':content_based,
            'collaborative':collaborative,
            'popularity':popular_queryset,
        }
        return render(request, 'index.html',context)

    
    
# def collaborative():
# import random
# from surprise import Reader, Dataset
# from surprise import SVD
# from surprise import NMF
# from surprise.model_selection import cross_validate
#     ratings_dict = {'productID': list(Rating.objects.values_list('product',flat=True)),
#             'userID': list(Rating.objects.values_list('user',flat=True)),
#             'rating': list(Rating.objects.values_list('rating', flat=True)),}
#     print(ratings_dict,'ratings_dict')
#     df = pd.DataFrame(ratings_dict)
#     print(df)
#     reader = Reader(rating_scale=(1, 5))
#     data = Dataset.load_from_df(df, reader)
#     print('--------------------------------------------------------data',data)
    

#     algo = SVD()
#     algo1=NMF()
#     res = cross_validate(algo, data, measures=['RMSE'])
#     res1 = cross_validate(algo1, data, measures=['RMSE'])
#     print(res,'----------------------------------------------------')
#     print(res1,'----------------------------------------------------')