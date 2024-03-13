import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from order_db import search_by_po_number,add_data,delete_data,find_data,update_data,search_by_part_number,get_status_data,draw_pie_chart
from material_db import return_mat_data,update_mat_data
from pay_db import add_pay_data,search_by_io_number,delete_pay_data,update_pay_data,calculate_payment_counts,draw_pie_chart_pay,find_pay_data
from tools_db import add_tool_data,update_tool_data,search_tool_by_po_number,search_tool_by_part_number

def main():
    menu = ['WELCOME', 'CURRENT DATA','STATISTICS','ORDER DETAILS', 'MATERIAL', 'TOOLS','PAYMENT DETAILS']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'WELCOME':
        st.markdown("<h1 style='text-align: center; color: #014421;'>WELCOME TO DASHBOARD</h1>", unsafe_allow_html=True)

    elif choice == 'CURRENT DATA':
        st.subheader("CURRENT DATA")
        df = find_data()
        if df:
            df=pd.DataFrame(df)
            df=df.drop('_id',axis=1)
            st.write(df)
        else:
            st.warning("NO DATA")

    elif choice=='STATISTICS':
        st.title("ORDER STATISTICS")
        status_data = get_status_data()
        st.plotly_chart(draw_pie_chart(status_data))
        df = find_data()
        if df:
            df=pd.DataFrame(df)
            status=st.selectbox('Sort By',['Choose','Incomplete','Ongoing','Completed','Delayed'])
            filtered_df = df[df['status'] == status]
            filtered_df=filtered_df.drop('_id',axis=1)
            st.write(filtered_df)
        else:
            st.warning("NO DATA")


    elif choice == "MATERIAL":
        st.subheader("MATERIAL DATA")
        
        # Radio button to choose between View Data and Update Data
        action = st.radio("Choose Action", ("View Data", "Update Data"))

        if action == "View Data":
            # Display expanders with current data
            with st.expander("Nickel-Graphite"):
                df = return_mat_data("Nickel-Graphite")
                if not df.empty:
                    df=df[['Material Composition','Material Required','Material Available']]
                    st.write(df)
                    fig = px.bar(df, x="Material Composition", y=["Material Available", "Material Required"],
                             title="Available vs Required", barmode="group",width=400,height=400)
                    st.plotly_chart(fig)

            with st.expander("Silver-Aluminium"):
                df = return_mat_data("Silver-Aluminium")
                if not df.empty:
                    df=df[['Material Composition','Material Required','Material Available']]
                    st.write(df)
                    fig = px.bar(df, x="Material Composition", y=["Material Available", "Material Required"],
                             title="Available vs Required", barmode="group",width=400,height=400)
                    st.plotly_chart(fig)


            with st.expander("Silver-Copper"):
                df = return_mat_data("Silver-Copper")
                if not df.empty:
                    df=df[['Material Composition','Material Required','Material Available']]
                    st.write(df)
                    fig = px.bar(df, x="Material Composition", y=["Material Available", "Material Required"],
                             title="Available vs Required", barmode="group",width=400,height=400)
                    st.plotly_chart(fig)

            with st.expander("Silver"):
                df = return_mat_data("Silver")
                if not df.empty:
                    df=df[['Material Composition','Material Required','Material Available']]
                    st.write(df)
                    fig = px.bar(df, x="Material Composition", y=["Material Available", "Material Required"],
                             title="Available vs Required", barmode="group",width=400,height=400)
                    st.plotly_chart(fig)


        elif action == "Update Data":
            # Display input fields to update data
            with st.expander("Nickel-Graphite"):
                col1,col2,col3=st.columns(3)
                with col1:
                    available = st.number_input("NiC Available", min_value=0, step=1)
                with col2:
                    required = st.number_input("NiC Required", min_value=0, step=1)
                with col3:
                    if(st.button('UPDATE NiC')):
                        if(update_mat_data("Nickel-Graphite",available,required)):
                            st.success('DATA UPDATED SUCCESSFULLY')
                        else:
                            st.warning("TRY AGAIN")
                

            with st.expander("Silver-Aluminium"):
                col1,col2,col3=st.columns(3)
                with col1:
                    available = st.number_input("Ag-Al Available", min_value=0, step=1)
                with col2:
                    required = st.number_input("Ag-Al Required", min_value=0, step=1)
                with col3:
                    if(st.button('UPDATE Ag-Al')):
                        if(update_mat_data("Silver-Aluminium",available,required)):
                            st.success('DATA UPDATED SUCCESSFULLY')
                        else:
                            st.warning("TRY AGAIN")
                

            with st.expander("Silver-Copper"):
                col1,col2,col3=st.columns(3)
                with col1:
                    available = st.number_input("Ag-Cu Available", min_value=0, step=1)
                with col2:
                    required = st.number_input("Ag-Cu Required", min_value=0, step=1)
                with col3:
                    if(st.button('UPDATE Ag-Cu')):
                        if(update_mat_data("Silver-Copper",available,required)):
                            st.success('DATA UPDATED SUCCESSFULLY')
                        else:
                            st.warning("TRY AGAIN")

            with st.expander("Silver"):
                col1,col2,col3=st.columns(3)
                with col1:
                    available = st.number_input("Ag Available", min_value=0, step=1)
                with col2:
                    required = st.number_input("Ag Required", min_value=0, step=1)
                with col3:
                    if(st.button('UPDATE Ag')):
                        if(update_mat_data("Silver",available,required)):
                            st.success('DATA UPDATED SUCCESSFULLY')
                        else:
                            st.warning("TRY AGAIN")


    elif choice == 'TOOLS':
        st.subheader("TOOLS")
        with st.expander("BROWSE TOOLS"):
            po_number = st.text_input(label="Search by PO number")
            if po_number:
                results = search_tool_by_po_number(po_number)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
        
            part_num = st.text_input(label="Search tool by Part number")
            if part_num:
                results = search_tool_by_part_number(part_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
        
        with st.expander("UPDATE TOOLS"):
            st.write("TOOLS")
            po_num = st.text_input('Enter PO Number')
            if po_num:
                results = search_tool_by_po_number(po_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
            part_num = st.text_input('Enter Part Number')
            if part_num:
                results = search_tool_by_part_number(part_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
            status = st.selectbox('Tool Status', ['Incomplete', 'Ongoing', 'Completed', 'Delayed'])
            if st.button("UPDATE TOOL"):
                if update_tool_data(po_num, status, part_num):
                    st.success("DATA UPDATED SUCCESSFULLY")
                else:
                    st.warning("TRY AGAIN")

        with st.expander("ADD TOOLS"):
            st.write("TOOLS")
            po_num=st.text_input(label='Type PO Number')
            po_date=st.date_input(label=" Type PO Date")
            part_nos=st.text_input(label="Type Part Numbers")
            tool_exis=st.selectbox("Tool Status",['Yes','No','Ordered'])
            tool_cost=st.number_input(label="Type Tool Cost")
            if st.button("ADD TOOL"):
                if(add_tool_data(po_num,po_date,part_nos,tool_exis,tool_cost)):
                    st.success("ADDED SUCCESSFULLY")
                else:
                    st.warning("TRY AGAIN")


    elif choice == 'ORDER DETAILS':
        st.subheader("ORDER DETAILS")
        action = st.radio("Choose Action", ("View Order", "Update Order","Add Order","Delete Order"))

        if action == "View Order":
            po_number = st.text_input(label="Search by PO number")
            if po_number:
                results = search_by_po_number(po_number)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
        
            part_num = st.text_input(label="Search by Part number")
            if part_num:
                results = search_by_part_number(part_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)

        elif action=='Add Order':
            po_num=st.text_input(label='PO Number')
            po_date=st.date_input(label="PO Date")
            loc=st.text_input(label="Location")
            deadline=st.date_input(label="Deadline")
            mat=st.text_input(label='Material')
            part_nos=st.text_input(label="Part Numbers")
            nos=st.number_input(label='Numbers') 
            po_val=st.number_input(label='PO Values')
            status=st.selectbox('Status',['Incomplete','Ongoing','Completed','Delayed'])

            if(st.button('ADD')):
                if(add_data(po_num, po_date, loc, deadline, mat, part_nos, nos, po_val, status)):
                    st.success('ORDER ADDED SUCCESSFULLY')
        
        elif action=="Delete Order":
            po_num=st.text_input('PO Number')
            if po_num:
                results = search_by_po_number(po_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
            
            part_num=st.text_input('Part Number')
            if part_num:
                results = search_by_part_number(part_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)

            if st.button("DELETE"):
                delete_data(po_num,part_num)
                st.success("ORDER DELETED SUCCESSFULLY")

        
        elif action=='Update Order':
            po_num=st.text_input('PO Number')
            if po_num:
                results = search_by_po_number(po_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
            
            part_num=st.text_input('Part Number')
            if part_num:
                results = search_by_part_number(part_num)
                if results.empty:  
                    st.warning('NO RECORDS FOUND')
                else:
                    st.write(results)
            
            status=st.selectbox('Status',['Incomplete','Ongoing','Completed','Delayed'])
            if st.button("UPDATE"):
                if(update_data(po_num,status,part_num)):
                    st.success("DATA UPDATED SUCCESSFULLY")
                else:
                    st.warning("TRY AGAIN")
    
    elif choice=='PAYMENT DETAILS':
        col1,col2=st.columns(2)
        with col1:
           st.title('PAYMENT GRAPH')
           df=calculate_payment_counts()
           if not df.empty: 
               st.plotly_chart(draw_pie_chart_pay(df))
                   
        with col2:
            st.title('PAYMENT DETAILS')
            with st.expander("ADD DETAILS"):
                i_no=st.text_input("Invoice Number")
                i_date=st.date_input("Invoice Date")
                amt=st.number_input("Payment Amount")
                stat=st.selectbox("Payment Status",['Done','Pending','Expected'])
                r_date=st.text_input("Received Date")
                if(st.button("ADD")):
                    if(add_pay_data(i_no,i_date,amt,stat,r_date)):
                        st.success("ADDED SUCCESSFULLY")
                    else:
                        st.warning("TRY AGAIN")
            with st.expander("UPDATE DETAILS"):
                i_no=st.text_input("Enter Invoice Number")
                if i_no:
                    results = search_by_io_number(i_no)
                    if results.empty:  
                        st.warning('NO RECORDS FOUND')
                    else:
                        st.write(results)
                if st.button("UPDATE"):
                    stat=st.selectbox("Payment Status",['Done','Pending','Expected'])
                    r_date=st.text_input("Received Date")
                    if st.button("UPDATE"):
                        if(update_pay_data(i_no,stat,r_date)):
                            st.success("UPDATED SUCCESSFULLY")
                        else:
                            st.warning("TRY AGAIN")

            with st.expander("DELETE "):
                i_no=st.number_input("Enter Invoice Number to Verify")
                if i_no:
                    results = search_by_io_number(i_no)
                    if results.empty:  
                        st.warning('NO RECORDS FOUND')
                    else:
                        st.warning("Sure,Wanna Delete?")
                        st.write(results)
                if st.button("DELETE"):
                    if(delete_pay_data(i_no)):
                        st.success("DELETED SUCCESSFULLY")
                    else:
                        st.warning("TRY AGAIN")

        st.title('PAYMENT DATA')
        # Calculate payment counts
        df1 = find_pay_data()
        # Data for the pie chart
        if not df1.empty: 
            df1=df1.drop('_id',axis=1)
            st.write(df1)
        else:
            st.warning("NO DATA")
        st.title('PAYMENT AMOUNT:')
        if not df.empty:
            total_payment_amount = df['Payment Amount'].sum() 
            st.subheader(total_payment_amount)


if __name__ =='__main__':
    main()
