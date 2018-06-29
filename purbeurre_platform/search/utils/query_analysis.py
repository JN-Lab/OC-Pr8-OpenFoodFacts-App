#! /usr/bin/env python3
# coding: utf-8
from functools import reduce
from ..models import Product, Category

class QueryAnalysis:
    """
    This class groups all the methods to check if the search terms asked
    by the user is linked to a product or a category registered in the database
    """
    
    def exists_in_category(self, query):
        """
        This method checked in Category model if there is one or several appropiate
        categories according the user query
        """


        words_query = query.lower().split()
        for word in words_query:
            pass


        if Category.objects.filter(name__icontains=query).exists():
            return True
        else:
            return False
