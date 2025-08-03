import streamlit as st
import json
import uuid
import random
from typing import List, Dict, Any
from pyairtable import Api
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Event Registration Dashboard",
    page_icon="🎉",
    layout="wide"
)

# Initialize session state
if 'event_data' not in st.session_state:
    st.session_state.event_data = {}

# Airtable configuration
AIRTABLE_CONFIG = {
    "base_id": "applJyRTlJLvUEDJs",
    "api_key": "patJHZQyID8nmSaxh.1bcf08f100bd723fd85d67eff8534a19f951b75883d0e0ae4cc49743a9fb3131"
}

def get_airtable_api():
    """Get Airtable API instance"""
    return Api(AIRTABLE_CONFIG["api_key"])

def get_airtable_table(table_name):
    """Get Airtable table instance"""
    api = get_airtable_api()
    return api.table(AIRTABLE_CONFIG["base_id"], table_name)

def generate_host_id():
    """Generate a random host ID"""
    return random.randint(1000, 9999)

def save_event(event_data):
    """Save event data to Airtable"""
    try:
        table = get_airtable_table("events")  # Assuming you have an events table
        
        record_data = {
            "name": event_data['name'],
            "description": event_data['description'],
            "host_id": event_data['host_id'],
            "location_name": event_data['location_name'],
            "detailed_address": event_data['detailed_address'],
            "start_date": event_data['start_date'].isoformat(),
            "end_date": event_data['end_date'].isoformat(),
            "capacity": event_data['capacity']
        }
        
        table.create(record_data)
        
        st.success("Etkinlik başarıyla kaydedildi!")
        return True
        
    except Exception as e:
        st.error(f"Etkinlik kaydedilirken hata oluştu: {str(e)}")
        return False

def validate_event_data(event_data):
    """Validate event data"""
    errors = []
    
    if not event_data.get('name'):
        errors.append("Etkinlik adı zorunludur")
    
    if not event_data.get('description'):
        errors.append("Etkinlik açıklaması zorunludur")
    
    if not event_data.get('location_name'):
        errors.append("Mekan adı zorunludur")
    
    if not event_data.get('detailed_address'):
        errors.append("Detaylı adres zorunludur")
    
    if not event_data.get('start_date'):
        errors.append("Başlangıç tarihi zorunludur")
    
    if not event_data.get('end_date'):
        errors.append("Bitiş tarihi zorunludur")
    
    if event_data.get('start_date') and event_data.get('end_date'):
        if event_data['start_date'] >= event_data['end_date']:
            errors.append("Bitiş tarihi başlangıç tarihinden sonra olmalıdır")
    
    if not event_data.get('capacity') or event_data['capacity'] <= 0:
        errors.append("Kapasite 0'dan büyük olmalıdır")
    
    return errors

def main():
    st.title("🎉 Etkinlik Kayıt Formu")
    st.markdown("Etkinliğinizi kaydetmek için aşağıdaki formu doldurun.")
    
    # Generate host_id
    host_id = generate_host_id()
    
    # Form sections
    with st.container():
        st.header("📝 Etkinlik Bilgileri")
        
        # Event name and description
        col1, col2 = st.columns(2)
        
        with col1:
            event_name = st.text_input(
                "Etkinlik Adı *",
                placeholder="Örn: Teknoloji Konferansı 2024",
                help="Etkinliğinizin adını girin"
            )
        
        with col2:
            capacity = st.number_input(
                "Kapasite *",
                min_value=1,
                value=50,
                help="Etkinliğinizin maksimum katılımcı sayısı"
            )
        
        # Description
        description = st.text_area(
            "Etkinlik Açıklaması *",
            placeholder="Etkinliğiniz hakkında detaylı bilgi verin...",
            height=100,
            help="Etkinliğinizin detaylı açıklamasını girin"
        )
        
        st.markdown("---")
        
        # Location information
        st.header("📍 Mekan Bilgileri")
        
        col3, col4 = st.columns(2)
        
        with col3:
            location_name = st.text_input(
                "Mekan Adı *",
                placeholder="Örn: İstanbul Kongre Merkezi",
                help="Etkinliğinizin gerçekleşeceği mekanın adı"
            )
        
        with col4:
            detailed_address = st.text_input(
                "Detaylı Adres *",
                placeholder="Örn: Harbiye Mah. Darülbedai Cad. No:3 Şişli/İstanbul",
                help="Etkinliğinizin tam adresi"
            )
        
        st.markdown("---")
        
        # Date and time information
        st.header("📅 Tarih ve Saat Bilgileri")
        
        col5, col6 = st.columns(2)
        
        with col5:
            start_date = st.date_input(
                "Başlangıç Tarihi *",
                value=datetime.now().date(),
                help="Etkinliğinizin başlangıç tarihi"
            )
            
            start_time = st.time_input(
                "Başlangıç Saati *",
                value=datetime.now().time(),
                help="Etkinliğinizin başlangıç saati"
            )
        
        with col6:
            end_date = st.date_input(
                "Bitiş Tarihi *",
                value=(datetime.now() + timedelta(days=1)).date(),
                help="Etkinliğinizin bitiş tarihi"
            )
            
            end_time = st.time_input(
                "Bitiş Saati *",
                value=(datetime.now() + timedelta(hours=2)).time(),
                help="Etkinliğinizin bitiş saati"
            )
        
        # Combine date and time
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)
        
        st.markdown("---")
        
        # Host information
        st.header("👤 Host Bilgileri")
        
        st.info(f"**Host ID:** {host_id} (Otomatik oluşturuldu)")
        
        # Preview section
        st.markdown("---")
        st.header("👁️ Önizleme")
        
        if event_name and description and location_name and detailed_address:
            st.markdown("**Etkinlik Özeti:**")
            
            col_preview1, col_preview2 = st.columns(2)
            
            with col_preview1:
                st.markdown(f"**Etkinlik Adı:** {event_name}")
                st.markdown(f"**Mekan:** {location_name}")
                st.markdown(f"**Kapasite:** {capacity} kişi")
                st.markdown(f"**Host ID:** {host_id}")
            
            with col_preview2:
                st.markdown(f"**Başlangıç:** {start_datetime.strftime('%d/%m/%Y %H:%M')}")
                st.markdown(f"**Bitiş:** {end_datetime.strftime('%d/%m/%Y %H:%M')}")
                st.markdown(f"**Adres:** {detailed_address}")
        
        # Submit button
        st.markdown("---")
        
        if st.button("🚀 Etkinliği Kaydet", type="primary", use_container_width=True):
            # Prepare event data
            event_data = {
                'name': event_name,
                'description': description,
                'host_id': host_id,
                'location_name': location_name,
                'detailed_address': detailed_address,
                'start_date': start_datetime,
                'end_date': end_datetime,
                'capacity': capacity
            }
            
            # Validate data
            errors = validate_event_data(event_data)
            
            if errors:
                st.error("Lütfen aşağıdaki hataları düzeltin:")
                for error in errors:
                    st.error(f"• {error}")
            else:
                if save_event(event_data):
                    # Clear form
                    st.session_state.event_data = {}
                    st.rerun()

if __name__ == "__main__":
    main() 