# COPYRIGHT 2022 MONOOCLE INSIGHTS
# ALL RIGHTS RESERVED
# UNAUTHORIZED USE, REPRODUCTION, OR
# DISTRIBUTION STRICTLY PROHIBITED
#
# AUTHOR: Sean O'Malley and Raymond Deiotte
# CREATION DATE: 20230802
# LAST UPDATED: 20230821

### Import Packages/Dependencies ###

# connection
import sys
# basic
from datetime import datetime
import paramiko
from io import BytesIO
import pandas as pd
import requests

### Query Data Class ###
class CareQueryData:

    def __init__(self, query, features, show = None):

        #FIXME
        # self.endpoint = 'http://localhost:5533/get_care_query'
        # self.endpoint = 'http://ec2-3-133-102-108.us-east-2.compute.amazonaws.com:5533/get_care_query'
        self.endpoint = 'http://CQBackendLB-1880313232.us-east-2.elb.amazonaws.com:5533/get_care_query'
        self.apikey = ''
        self.length = None
        self.features = features

        self.query = query
        
        if show != False:
            self.summary = self.summarize(show)

    def summarize(self, show = None):
        
        # un-nest
        features = self.query

        # show criterion
        if str(features["query"]) in ["encounter", "visit", "journey", "episode"]:
        
            query_text = str(features["query"]).replace("_"," ")
            min_date_text = str(features["min_date"])
            max_date_text = str(features["max_date"])
            gender_text = str(features["gender"]).replace("[","").replace("]","").replace(","," and ").replace("m","Males").replace("f","Females")
            age_min_text = features["age_min"]
            age_max_text = features["age_max"]

            if features["limit"] != None:
                limit_text = "Query will return the top " + "{:,.0f}".format(features["limit"]) + " rows meeting the query criterion."
            else:
                limit_text = "No Volume Limit: query will return ALL results"

            # dynamic warning list
            if features["warnings"] != None:
                
                try:
                    warnings_list_text2a = features["warnings"][0]
                    warnings_list_text = f"""
                    Query Logic:

                    {warnings_list_text2a}

                    ---------------"""
                except:
                    next
                try:
                    warnings_list_text2b = features["warnings"][1]
                    warnings_list_text = f"""
                    Query Logic:

                    {warnings_list_text2a}
                    {warnings_list_text2b}

                    ---------------"""
                except:
                    next
                try:
                    warnings_list_text2c = features["warnings"][2]
                    warnings_list_text = f"""
                    Query Logic:

                    {warnings_list_text2a}
                    {warnings_list_text2b}
                    {warnings_list_text2c}

                    ---------------"""
                except:
                    next
                try:
                    warnings_list_text2d = features["warnings"][3]
                    warnings_list_text = f"""
                    Query Logic:

                    {warnings_list_text2a}
                    {warnings_list_text2b}
                    {warnings_list_text2c}
                    {warnings_list_text2d}

                    ---------------"""
                except:
                    next
                try:
                    warnings_list_text2e = features["warnings"][4]
                    warnings_list_text = f"""
                    Query Logic:

                    {warnings_list_text2a}
                    {warnings_list_text2b}
                    {warnings_list_text2c}
                    {warnings_list_text2d}
                    {warnings_list_text2e}

                    ---------------"""
                except:
                    next
                try:
                    warnings_list_text2f = features["warnings"][5]
                    warnings_list_text = f"""
                    Query Logic:

                    {warnings_list_text2a}
                    {warnings_list_text2b}
                    {warnings_list_text2c}
                    {warnings_list_text2d}
                    {warnings_list_text2e}
                    {warnings_list_text2f}
                    ...
                    ---------------"""
                except:
                    next
            else:
                warnings_list_text = "No Query Warnings Flagged"

            # state
            if (features["state"] != None):
                state_text = f"""from any of the below states:
                    {str(features["state"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                state_text = ""

            # short zip
            if (features["short_zip"] != None):
                if (features["state"] != None):
                    zip_text = f"""or any of the below zip codes:
                    {str(features["short_zip"]).replace(", "," or ").replace("[","").replace("]","")}"""
                else:
                    zip_text = f"""from any of the below zip codes:
                    {str(features["short_zip"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                zip_text = ""

            # if non, then all
            if (zip_text == "") & (state_text == ""):
                state_text = "Any/All Geographies Available to User's Access Plan Will be Queried"
                
            # create operand based on greedy preferences 
            if features["greedy"] != False:
                operand = "--- OR ---"
            else:
                operand = "--- AND ---"

            # visit type
            if features["visit_type"] != None:
                if any(isinstance(el, list) for el in features["visit_type"]):
                    try:
                        visit_type_text = f"""Visit Type(s):
                    {str(features["visit_type"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        visit_type_text = f"""Visit Type(s):
                    {str(features["visit_type"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        visit_type_text = f"""Visit Type(s):
                    {str(features["visit_type"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        visit_type_text = f"""Visit Type(s):
                    {str(features["visit_type"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        visit_type_text = f"""Visit Type(s):
                    {str(features["visit_type"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["visit_type"][4]).replace(", "," or ").replace("[","").replace("]","")}
                    ..."""
                    except:
                        next
                else:
                    visit_type_text = f"""Visit Type(s):
                    {str(features["visit_type"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                visit_type_text = "Any/All Corresponding Visit Type(s)"

            # payor channels
            if features["payor_channel"] != None:
                if any(isinstance(el, list) for el in features["payor_channel"]):
                    try:
                        payor_channel_text = f"""Payor Channel(s):
                    {str(features["payor_channel"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        payor_channel_text = f"""Payor Channel(s):
                    {str(features["payor_channel"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        payor_channel_text = f"""Payor Channel(s):
                    {str(features["payor_channel"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        payor_channel_text = f"""Payor Channel(s):
                    {str(features["payor_channel"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        payor_channel_text = f"""Payor Channel(s):
                    {str(features["payor_channel"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["payor_channel"][4]).replace(", "," or ").replace("[","").replace("]","")}
                    ..."""
                    except:
                        next
                else:
                    payor_channel_text = f"""Payor Channel(s):
                    {str(features["payor_channel"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                payor_channel_text = "Any/All Corresponding Payor Channel(s)"

            # revenue center codes
            if features["revenue_center_code"] != None:
                if any(isinstance(el, list) for el in features["revenue_center_code"]):
                    try:
                        revenue_center_code_text = f"""Revenue Center Code(s):
                    {str(features["revenue_center_code"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        revenue_center_code_text = f"""Revenue Center Code(s):
                    {str(features["revenue_center_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        revenue_center_code_text = f"""Revenue Center Code(s):
                    {str(features["revenue_center_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        revenue_center_code_text = f"""Revenue Center Code(s):
                    {str(features["revenue_center_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        revenue_center_code_text = f"""Revenue Center Code(s):
                    {str(features["revenue_center_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["revenue_center_code"][4]).replace(", "," or ").replace("[","").replace("]","")}
                    ..."""
                    except:
                        next
                else:
                    revenue_center_code_text = f"""Revenue Center Code(s):
                    {str(features["revenue_center_code"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                revenue_center_code_text = "Any/All Corresponding Revenue Center Code(s)"

            # place of service
            if features["place_of_service"] != None:
                if any(isinstance(el, list) for el in features["place_of_service"]):
                    try:
                        place_of_service_text = f"""Place(s) of Service:
                    {str(features["place_of_service"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        place_of_service_text = f"""Place(s) of Service:
                    {str(features["place_of_service"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        place_of_service_text = f"""Place(s) of Service:
                    {str(features["place_of_service"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        place_of_service_text = f"""Place(s) of Service:
                    {str(features["place_of_service"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        place_of_service_text = f"""Place(s) of Service:
                    {str(features["place_of_service"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["place_of_service"][4]).replace(", "," or ").replace("[","").replace("]","")}
                    ..."""
                    except:
                        next
                else:
                    place_of_service_text = f"""Place(s) of Service:
                    {str(features["place_of_service"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                place_of_service_text = "Any/All Corresponding Place(s) of Service"

            # drg
            # if features["drg_code"] != None:
            #     if any(isinstance(el, list) for el in features["drg_code"]):
            #         try:
            #             drg_code_text = f"""DRGs - Diagnosis Related Group(s):
            #         {str(features["drg_code"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
            #         except:
            #             next
            #         try:
            #             drg_code_text = f"""DRGs - Diagnosis Related Group(s):
            #         {str(features["drg_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
            #         except:
            #             next
            #         try:
            #             drg_code_text = f"""DRGs - Diagnosis Related Group(s):
            #         {str(features["drg_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
            #         except:
            #             next
            #         try:
            #             drg_code_text = f"""DRGs - Diagnosis Related Group(s):
            #         {str(features["drg_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
            #         except:
            #             next
            #         try:    
            #             drg_code_text = f"""DRGs - Diagnosis Related Group(s):
            #         {str(features["drg_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][3]).replace(", "," or ").replace("[","").replace("]","")}
            #         and
            #         {str(features["drg_code"][4]).replace(", "," or ").replace("[","").replace("]","")}
            #         ..."""
            #         except:
            #             next
            #     else:
            #         drg_code_text = f"""DRGs - Diagnosis Related Group(s):
            #         {str(features["drg_code"]).replace(", "," or ").replace("[","").replace("]","")}"""
            # else:
            #     drg_code_text = "Any/All Corresponding DRGs - Diagnosis Related Group(s)"

            # diagnosis code
            if features["diag_code"] != None:
                if any(isinstance(el, list) for el in features["diag_code"]):
                    try:
                        diag_code_text = f"""Diagnosis Code(s):
                    {str(features["diag_code"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        diag_code_text = f"""Diagnosis Code(s):
                    {str(features["diag_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        diag_code_text = f"""Diagnosis Code(s):
                    {str(features["diag_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        diag_code_text = f"""Diagnosis Code(s):
                    {str(features["diag_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        diag_code_text = f"""Diagnosis Code(s):
                    {str(features["diag_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["diag_code"][4]).replace(", "," or ").replace("[","").replace("]","")}
                    ..."""
                    except:
                        next
                else:
                    diag_code_text = f"""Diagnosis Code(s):
                    {str(features["diag_code"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                diag_code_text = "Any/All Corresponding Diagnosis Codes"

            # procedure code
            if features["proc_code"] != None:
                if any(isinstance(sub, list) for sub in features["proc_code"]):
                    try:
                        proc_code_text = f"""Procedure(s):
                    {str(features["proc_code"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        proc_code_text = f"""Procedure(s):
                    {str(features["proc_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        proc_code_text = f"""Procedure(s):
                    {str(features["proc_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        proc_code_text = f"""Procedure(s):
                    {str(features["proc_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        proc_code_text = f"""Procedure(s):
                    {str(features["proc_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["proc_code"][4]).replace(", "," or ").replace("[","").replace("]","")}
                    ..."""
                    except:
                        next
                else:
                    proc_code_text = f"""Procedure(s):
                    {str(features["proc_code"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                    proc_code_text = "Any/All Corresponding Procedure Codes"

            # taxonomy code
            if features["taxonomy_code"] != None:
                if any(isinstance(sub, list) for sub in features["taxonomy_code"]):
                    try:
                        taxonomy_code_text = f"""Taxonomy Code(s):
                    {str(features["taxonomy_code"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        taxonomy_code_text = f"""Taxonomy Code(s):
                    {str(features["taxonomy_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["taxonomy_code"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        taxonomy_code_text = f"""Taxonomy Code(s):
                    {str(features["taxonomy_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["taxonomy_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["taxonomy_code"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        taxonomy_code_text = f"""Taxonomy Code(s):
                    {str(features["taxonomy_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["taxonomy_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["taxonomy_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["taxonomy_code"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        taxonomy_code_text = f"""Taxonomy Code(s):
                        {str(features["taxonomy_code"][0]).replace(", "," or ").replace("[","").replace("]","")}
                        and
                        {str(features["taxonomy_code"][1]).replace(", "," or ").replace("[","").replace("]","")}
                        and
                        {str(features["taxonomy_code"][2]).replace(", "," or ").replace("[","").replace("]","")}
                        and
                        {str(features["taxonomy_code"][3]).replace(", "," or ").replace("[","").replace("]","")}
                        and
                        {str(features["taxonomy_code"][4]).replace(", "," or ").replace("[","").replace("]","")}
                        ..."""
                    except:
                        next
                else:
                    taxonomy_code_text = f"""Taxonomy Code(s):
                    {str(features["taxonomy_code"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                    taxonomy_code_text = "Any/All Corresponding (Specialty) Taxonomy Codes"

            # referring npis
            if features["ref_npi"] != None:
                if any(isinstance(el, list) for el in features["ref_npi"]):
                    try:
                        ref_npi_text = f"""Referring NPI(s):
                    {str(features["ref_npi"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        ref_npi_text = f"""Referring NPI(s):
                    {str(features["ref_npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        ref_npi_text = f"""Referring NPI(s):
                    {str(features["ref_npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        ref_npi_text = f"""Referring NPI(s):
                    {str(features["ref_npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        ref_npi_text = f"""Referring NPI(s):
                    {str(features["ref_npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["ref_npi"][4]).replace(", "," or ").replace("[","").replace("]","")}
                            ..."""
                    except:
                        next
                else:
                    ref_npi_text = f"""Referring NPI(s):
                    {str(features["ref_npi"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                ref_npi_text = "Any/All Corresponding Referring NPI(s)"

            #  npis
            if features["npi"] != None:
                if any(isinstance(el, list) for el in features["npi"]):
                    try:
                        npi_text = f"""NPI(s) - National Provider Identifier(s):
                    {str(features["npi"][0]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        npi_text = f""":
                    {str(features["npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][1]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        npi_text = f"""NPI(s) - National Provider Identifier(s):
                    {str(features["npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][2]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:
                        npi_text = f"""NPI(s) - National Provider Identifier(s):
                    {str(features["npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][3]).replace(", "," or ").replace("[","").replace("]","")}"""
                    except:
                        next
                    try:    
                        npi_text = f"""NPI(s) - National Provider Identifier(s):
                    {str(features["npi"][0]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][1]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][2]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][3]).replace(", "," or ").replace("[","").replace("]","")}
                    and
                    {str(features["npi"][4]).replace(", "," or ").replace("[","").replace("]","")}
                            ..."""
                    except:
                        next
                else:
                    npi_text = f"""NPI(s) - National Provider Identifier(s):
                    {str(features["npi"]).replace(", "," or ").replace("[","").replace("]","")}"""
            else:
                npi_text = "Any/All Corresponding NPI(s) - National Provider Identifier(s)"

            self.summary = f"""
                    ---------------------------------------------------------------------------------------------------------
                    ---------------------------------------------------------------------------------------------------------
                    {query_text.title()} Query Summary
                    (specify 'show = False' within query method to suppress message)
                    ---------------------------------------------------------------------------------------------------------
                    ---------------------------------------------------------------------------------------------------------
                    {warnings_list_text} 

                    Query Volume Limit: 
                    {limit_text} 

                    ---------------

                    Query will return line-item granularity for {query_text}s from {min_date_text} to {max_date_text} that meet the following criterion...

                    Population: 

                    {gender_text} patients between the ages of {age_min_text} and {age_max_text} 

                    {state_text} 
                    {zip_text}

                    Specifications:

                    {visit_type_text}

                    {operand}

                    {payor_channel_text}

                    {operand}

                    {revenue_center_code_text}

                    {operand}

                    {place_of_service_text}

                    {operand}

                    {diag_code_text}

                    {operand}

                    {proc_code_text}

                    {operand}

                    {taxonomy_code_text}

                    {operand}

                    {ref_npi_text}

                    {operand}

                    {npi_text}

                    ---------------------------------------------------------------------------------------------------------
                    ---------------------------------------------------------------------------------------------------------
                            """

            if show == True:
                
                print(self.summary)

        else:

            print(features)

    def estimate(self, as_pandas = None):

        # update mode
        self.query.update({"mode":"estimate"})
        self.query.update({"timestamp":datetime.now().strftime('%Y%m%d_%H%M%S')})

        # execute to SFTP, inform user
        if self.query["query"] in ["journey", "visit", "episode", "encounter", "script-encounter", "script-journey"]:
            self.info = self.sendRequest("estimate")
            print("--------")
            print("   ")
            print(f"""{self.query["query"]} query results will be returned to the SFTP location specified below. You will be notified of query completion via email.""")
            print("   ")
            print("--------")
            print(self.info)
            print("*** query status has been written to query_object_name.info ***")
            print("Upon query completion to SFTP location, you may execute query_object_name.sftpToPandas() to read data into pandas DataFrame")
            print("--------")
            return self.info
        # return locally
        else:
            self.data = self.sendRequest("estimate")
            print("--------")
            print("   ")
            print("Query has been executed and returned locally")
            print("*** query output has been written to query_object_name.data ***")
            print("   ")
            print("--------")
            # return as pandas dataframe
            if as_pandas != False:
                self.data = pd.DataFrame(self.data)
            return self.data
        
    def sample(self, as_pandas = None):

        # update mode
        self.query.update({"mode":"sample"})
        self.query.update({"timestamp":datetime.now().strftime('%Y%m%d_%H%M%S')})

        # execute to SFTP, inform user
        if self.query["query"] in ["journey", "visit", "episode", "encounter", "script-encounter", "script-journey"]:
            self.info = self.sendRequest("sample")
            print("--------")
            print("   ")
            print(f"""{self.query["query"]} query results will be returned to the SFTP location specified below. You will be notified of query completion via email.""")
            print("   ")
            print("--------")
            print(self.info)
            print("*** query status has been written to query_object_name.info ***")
            print("Upon query completion to SFTP location, you may execute query_object_name.sftpToPandas() to read data into pandas DataFrame")
            print("--------")
            return self.info
        # return locally
        else:
            self.data = self.sendRequest("sample")
            print("--------")
            print("   ")
            print("Query has been executed and returned locally")
            print("*** query output has been written to query_object_name.data ***")
            print("   ")
            print("--------")
            # return as pandas dataframe
            if as_pandas != False:
                self.data = pd.DataFrame(self.data)
            return self.data
        
    def execute(self, as_pandas = None):

        # update mode
        self.query.update({"mode":"execute"})
        self.query.update({"timestamp":datetime.now().strftime('%Y%m%d_%H%M%S')})

        # execute to SFTP, inform user
        if self.query["query"] in ["journey", "visit", "episode", "encounter", "script-encounter", "script-journey"]:
            self.info = self.sendRequest()
            print("--------")
            print("   ")
            print(f"""{self.query["query"]} query results will be returned to the SFTP location specified below. You will be notified of query completion via email.""")
            print("   ")
            print("--------")
            print(self.info)
            print("*** query status has been written to query_object_name.info ***")
            print("Upon query completion to SFTP location, you may execute query_object_name.sftpToPandas() to read data into pandas DataFrame")
            print("--------")

            return self.info

        # execute to local, inform user
        else:
            self.data = self.sendRequest()
            print("--------")
            print("   ")
            print("Query has been executed and returned locally")
            print("*** query output has been written to query_object_name.data ***")
            print("   ")
            print("--------")

            # return as pandas dataframe
            if as_pandas != False:
                self.data = pd.DataFrame(self.data)

            return self.data

    def sendRequest(self, type = None):
        '''
        Method to send the request to the CQ API Endpoint
        @param data:
        @return:
        '''
        response = requests.post(self.endpoint, json=self.query)

        self.data = None
        #TODO - get the payload back r.data?
        if response.status_code == 200:
            if type == "estimate":
                print(f'Successfully calculated the size of the query...')
                self.data = response.json()
            elif type == "sample":
                print("---")
                print(f'Successfully made a sample of the query...')
                self.data = response.json()
                print("---")
            else:
                print("---")
                print(f'Successfully executed the query...')
                self.data = response.json()
                print("---")
        else:
            if type == "estimate":
                print(f"Failed to execute the query: {response}")
            elif type == "sample":
                print(f"Failed to execute a sample of the query: {response}")
            else:
                print(f"Failed to execute the query: {response}")

        return self.data

    def sftpToPandas(self, hostname, username, private_key_path, remote_path):
        
        """Downloads Parquet files from SFTP using public key authentication."""

        # Create an SSH client instance.
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh_client.connect(hostname, username=username, pkey=private_key)

        # Create an SFTP client from the SSH client
        sftp_client = ssh_client.open_sftp()

        # List all files in the remote directory
        file_list = sftp_client.listdir(remote_path)

        # Filter for Parquet files
        parquet_files = [file for file in file_list if file.endswith('.parquet')]

        dataframes = []
        for file in parquet_files:
            file_path = f"{remote_path}/{file}"
            with sftp_client.open(file_path, 'rb') as remote_file:
                file_content = remote_file.read()
                df = pd.read_parquet(BytesIO(file_content))
                dataframes.append(df)

        # Concatenate all dataframes
        self.data = pd.concat(dataframes, ignore_index=True)

        # Close SFTP and SSH connections
        sftp_client.close()
        ssh_client.close()

        return self.data