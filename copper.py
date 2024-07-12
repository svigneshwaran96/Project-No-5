import streamlit as st
from streamlit_option_menu import option_menu

import numpy as np
import pickle


#set up page configuration for streamlit
icon='https://st2.depositphotos.com/1000128/7250/i/450/depositphotos_72503649-stock-photo-copper-pipes.jpg'
st.set_page_config(page_title='Industrial copper',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide',menu_items={"about":'This streamlit application was developed by M.Gokul'})


#set up the sidebar with optionmenu
with st.sidebar:
    selected = option_menu("MainMenu",
                            options=["Home","Get Prediction","About"],
                            icons=["house","lightbulb","info-circle"],
                            default_index=1,
                            orientation="vertical",)

#user input values for selectbox and encoded for respective features
class option():
    
    country_values=[ 25.,  26.,  27.,  28.,  30.,  32.,  38.,  39.,  40.,  77.,  78., 79.,  80.,  84.,  89., 107., 113.]

    status_values=['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM','Wonderful', 'Revised',
            'Offered', 'Offerable']

    status_encoded = {'Lost':0, 'Won':1, 'Draft':2, 'To be approved':3, 'Not lost for AM':4,'Wonderful':5, 'Revised':6,
                    'Offered':7, 'Offerable':8}
    
    item_type_values=['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']

    item_type_encoded = {'W':5.0, 'WI':6.0, 'S':3.0, 'Others':1.0, 'PL':2.0, 'IPL':0.0, 'SLAWR':4.0}

    application_values=[2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0, 26.0, 27.0, 28.0, 29.0, 38.0, 39.0, 40.0,
                41.0, 42.0, 56.0, 58.0, 59.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 99.0]
    
    product_ref_values=[611728, 611733, 611993, 628112, 628117, 628377, 640400, 640405, 640665, 164141591, 164336407,
                164337175, 929423819, 1282007633, 1332077137, 1665572032, 1665572374, 1665584320, 1665584642,
                1665584662, 1668701376, 1668701698, 1668701718, 1668701725, 1670798778, 1671863738, 1671876026,
                1690738206, 1690738219, 1693867550, 1693867563, 1721130331, 1722207579]

#set up information for the 'get prediction' menu
if selected == 'Get Prediction':
    title_text = '''<h1 style='font-size: 32px;text-align: center;color:grey;'>Copper Selling Price and Status Prediction</h1>'''
    st.markdown(title_text, unsafe_allow_html=True)
    
    #set up option menu for selling price and status menu
    select=option_menu('',options=["Selling Price","Status"],
                                    icons=["cash", "toggles"],
                                    orientation='horizontal',)


    if select == 'Selling Price':
        st.markdown("<h5 style=color:grey>To predict the selling price of copper, please provide the following information:",unsafe_allow_html=True)
        st.write('')

        # creted form to get the user input 
        with st.form('prediction'):
            col1,col2=st.columns(2)
            with col1:

                item_date=st.date_input(label='Item Date',format='DD/MM/YYYY')

                country=st.selectbox(label='Country',options=option.country_values,index=None)

                item_type=st.selectbox(label='Item Type',options=option.item_type_values,index=None)

                application=st.selectbox(label='Application',options=option.application_values,index=None)

                product_ref=st.selectbox(label='Product Ref',options=option.product_ref_values,index=None)

                customer=st.number_input('Customer ID',min_value=10000)

            with col2:

                delivery_date=st.date_input(label='Delivery Date',format='DD/MM/YYYY')

                status=st.selectbox(label='Status',options=option.status_values,index=None)

                quantity=st.number_input(label='Quantity',min_value=0.1)

                width=st.number_input(label='Width',min_value=1.0)

                thickness=st.number_input(label='Thickness',min_value=0.1)

                st.markdown('<br>', unsafe_allow_html=True)
                
                button=st.form_submit_button('PREDICT',use_container_width=True)

        if button:
            #check whether user fill all required fields
            if not all([item_date, delivery_date, country, item_type, application, product_ref,
                        customer, status, quantity, width, thickness]):
                st.error("Please fill in all required fields.")

            else:
                
                #opened pickle model and predict the selling price with user data
                with open('Regressor.pkl','rb') as files:
                    predict_model=pickle.load(files)

                # customize the user data to fit the feature 
                status=option.status_encoded[status]
                item_type=option.item_type_encoded[item_type]

                delivery_time_taken=abs((item_date - delivery_date).days)

                quantity_log=np.log(quantity)
                thickness_log=np.log(thickness)

                #predict the selling price with regressor model
                user_data=np.array([[customer, country, status, item_type ,application, width, product_ref,
                                    delivery_time_taken, quantity_log, thickness_log ]])
                
                pred=predict_model.predict(user_data)

                selling_price=np.exp(pred[0])

                #display the predicted selling price 
                st.subheader(f":green[Predicted Selling Price :] {selling_price:.2f}") 
                st.balloons()

    if select == 'Status':
        st.markdown("<h5 style=color:grey;>To predict the status of copper, please provide the following information:",unsafe_allow_html=True)
        st.write('')

        #creted form to get the user input 
        with st.form('classifier'):
            col1,col2=st.columns(2)
            with col1:

                item_date=st.date_input(label='Item Date',format='DD/MM/YYYY')

                country=st.selectbox(label='Country',options=option.country_values,index=None)

                item_type=st.selectbox(label='Item Type',options=option.item_type_values,index=None)

                application=st.selectbox(label='Application',options=option.application_values,index=None)

                product_ref=st.selectbox(label='Product Ref',options=option.product_ref_values,index=None)

                customer=st.number_input('Customer ID',min_value=10000)

            with col2:

                delivery_date=st.date_input(label='Delivery Date',format='DD/MM/YYYY')

                quantity=st.number_input(label='Quantity',min_value=0.1)

                width=st.number_input(label='Width',min_value=1.0)

                thickness=st.number_input(label='Thickness',min_value=0.1)

                selling_price=st.number_input(label='Selling Price',min_value=0.1)

                st.markdown('<br>', unsafe_allow_html=True)
                
                button=st.form_submit_button('PREDICT',use_container_width=True)

        if button:
            #check whether user fill all required fields
            if not all([item_date, delivery_date, country, item_type, application, product_ref,
                        customer,quantity, width, thickness,selling_price]):
                st.error("Please fill in all required fields.")

            else:
                #opened pickle model and predict status with user data
                with open('Classifier.pkl','rb') as files:
                    model=pickle.load(files)

                # customize the user data to fit the feature 
                item_type=option.item_type_encoded[item_type]

                delivery_time_taken=abs((item_date - delivery_date).days)

                quantity_log=np.log(quantity)
                thickness_log=np.log(thickness)
                selling_price_log=np.log(selling_price)

                #predict the status with classifier model
                user_data=np.array([[customer, country, item_type ,application, width, product_ref,
                                    delivery_time_taken, quantity_log, thickness_log, selling_price_log ]])
                
                status=model.predict(user_data)

                #display the predicted status 
                if status==1:
                    st.subheader(f":green[Status of the copper : ] Won")

                else:
                    st.subheader(f":red[Status of the copper :] Lost")


# set up the information for 'Home' menu
if selected == 'Home':
    title_text = '''<h1 style='font-size: 30px;text-align: center; color:grey;'>INDUSTRIAL COPPER</h1>'''
    st.markdown(title_text, unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.subheader(':blue[What is copper?]')

        st.markdown('''<h5 style='color:grey;font-size:21px'> Copper is a reddish brown metal that is found in abundance all around the world, 
                    while the top three producers are Chile, Peru, and China. Historically, copper was the first metal to be worked 
                    by human hands. When we discovered that it could be hardened with tin to make bronze around 3000 BC,
                    the Bronze Age was ushered in, changing the course of humanity.''',unsafe_allow_html=True)

    with col2:
        st.image('https://st2.depositphotos.com/1000128/7250/i/450/depositphotos_72503649-stock-photo-copper-pipes.jpg')

    st.subheader(':blue[What Is Copper Used For?]')
    st.markdown('''<h5 style='color:grey;font-size:20px'>According to the Copper Development Association (CDA) there 
                are four different areas of industry where copper is utilized:<br>
                - Electrical: 65% <br>
                - Construction: 25% <br>
                - Transport: 7% <br>
                - Other: 3% ''',unsafe_allow_html=True)
    with st.container():
        with st.expander(':blue[***Electrical Copper***]'):
            st.markdown('''<h6 style='color:grey;font-size:18px'>Copper is used in virtually all electrical wiring (except for power lines, 
                        which are made with aluminum) because it is the second most electrically conductive metal aside from silver 
                        which is much more expensive. In addition to being widely available and inexpensive, it is malleable and easy to
                        stretch out into very thin, flexible but strong wires, making it ideal to use in electrical infrastructure.<br>Aside from 
                        electrical wiring,copper is also used in heating elements, motors, renewable energy, internet lines, and electronics.
                        ''',unsafe_allow_html=True)
    with st.container():
        with st.expander(':blue[***Copper for Construction, Piping, & Design***]'):
            st.markdown('''<h6 style='color:grey;font-size:18px'>Copper has been used as construction material for centuries. 
                        It develops a characteristic beautiful green patina, or verdigris, that was highly desired in certain architectural styles, 
                        and still is to this day. Copper is still used today in architecture due to its corrosion resistance, easy workability, 
                        and attractiveness; copper sheets make a beautiful roofing material and other exterior features on buildings.
                        On the interior, copper is used in door handles, trim, vents, railings, kitchen appliances and cookware, 
                        lighting fixtures, and more.''',unsafe_allow_html=True)
            
    with st.container():
        with st.expander(':blue[***Use of Copper in Transportation***]'):
            st.markdown('''<h6 style='color:grey;font-size:18px'>Aside from the copper wiring used in the electrical components of modern cars, copper 
                        and brass have been the industry standard for oil coolers and radiators since the 1970s. Alloys that include copper are used 
                        in the locomotive and aerospace industries as well. As demand for electric cars and other forms of transportation increases,
                        demand for copper components also increases.''',unsafe_allow_html=True)
            
    with st.container():
        with st.expander(':blue[***Other Copper Uses***]'):
            st.markdown('''<h6 style='color:grey;font-size:18px'>Because copper is a beautiful, easily worked material, it is used in art such as copper
                        sheet metal sculptures, jewelry, signage, musical instruments, cookware, and more. The Statue of Liberty, is plated with more than
                        80 tons of copper, which gives her the characteristic pale green patina. Due to its antimicrobial properties, copper is also starting 
                        to gain popularity for high-touch items such as faucets, doorknobs, latches, railings, counters, hooks, handles, and other public 
                        surfaces that tend to gather a lot of germs.''',unsafe_allow_html=True)

    st.link_button('More about copper',url='https://en.wikipedia.org/wiki/Copper')

    col1,col2=st.columns(2)
    with col1:
            st.video('https://www.youtube.com/watch?v=gqmkiPPIsUQ&pp=ygUNIGFib3V0IGNvcHBlcg%3D%3D')
    with col2:
            st.video('https://www.youtube.com/watch?v=AgRYHT6WFV0&pp=ygUTIGNvcHBlciBpbiBpbmR1c3RyeQ%3D%3D')


#set up information for 'About' menu 
if selected == "About":
    st.subheader(':blue[Project Title :]')
    st.markdown('<h5> Industrial Copper Modeling',unsafe_allow_html=True)

    st.subheader(':blue[Domain :]')
    st.markdown('<h5> Manufacturing ',unsafe_allow_html=True)

    st.subheader(':blue[Skills & Technologies :]')
    st.markdown('<h5> Python scripting, Data Preprocessing, Machine learning, EDA, Streamlit ',unsafe_allow_html=True)

    st.subheader(':blue[Overview :]')
    st.markdown('''  <h5>Data Preprocessing:  <br>     
                <li>Loaded the copper CSV into a DataFrame. <br>              
                <li>Cleaned and filled missing values, addressed outliers, and adjusted data types.  <br>           
                <li>Analyzed data distribution and treated skewness.''',unsafe_allow_html=True)
    st.markdown(''' <h5>Feature Engineering: <br>
                <li>Assessed feature correlation to identify potential multicollinearity ''',unsafe_allow_html=True)
    st.markdown('''<h5>Modeling: <br>
                <li >Built a regression model for selling price prediction.
                <li>Built a classification model for status prediction.
                <li>Encoded categorical features and optimized hyperparameters.
                <li>Pickled the trained models for deployment.''',unsafe_allow_html=True)
    st.markdown('''<h5>Streamlit Application: <br>
                <li>Developed a user interface for interacting with the models.
                <li>Predicted selling price and status based on user input.''',unsafe_allow_html=True)
    st.subheader(':blue[About :]')
    st.markdown('''**Hello! I'm Gokul, a MBA graduate with a keen interest in data science and analytics.
                Currently on an exciting journey into the world of data science...**''')
    st.link_button('Linkedin','https://www.linkedin.com/in/gokul-m-j17/') 
