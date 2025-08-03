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

def get_record_by_host_id(host_id):
    """Get record by host_id to retrieve the ID column value"""
    try:
        table = get_airtable_table("events")
        # Search for records with the specific host_id
        # Try different formula syntax
        try:
            records = table.all(formula=f"{{host_id}} = '{host_id}'")
        except:
            # Fallback: get all records and filter
            records = table.all()
            records = [r for r in records if r.get('fields', {}).get('host_id') == host_id]
        
        if records and len(records) > 0:
            # Get the most recent record (last created)
            latest_record = records[-1]
            fields = latest_record.get('fields', {})
            
            # Look for ID column in fields
            if 'ID' in fields:
                return fields['ID']
            elif 'id' in fields:
                return fields['id']
            elif 'Id' in fields:
                return fields['Id']
            else:
                return None
        
        return None
    except Exception as e:
        st.error(f"ID Column Value alınırken hata oluştu: {e}")
        return None

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
        
        # Create the record
        response = table.create(record_data)
        
        if response:
            st.success("✅ Etkinlik başarıyla kaydedildi!")
            
            # Handle different response structures
            record_id = None
            
            # If response is a dict, it might contain the record directly
            if isinstance(response, dict):
                # Check if it has a 'fields' field with ID column
                if 'fields' in response:
                    fields = response['fields']
                    # Look for ID column in fields
                    if 'ID' in fields:
                        record_id = fields['ID']
                        st.success(f"📋 ID Column Value (from response): {record_id}")
                        return record_id
                    elif 'id' in fields:
                        record_id = fields['id']
                        st.success(f"📋 ID Column Value (from response): {record_id}")
                        return record_id
                    elif 'Id' in fields:
                        record_id = fields['Id']
                        st.success(f"📋 ID Column Value (from response): {record_id}")
                        return record_id
                # Check if it has a 'records' field
                elif 'records' in response and len(response['records']) > 0:
                    record = response['records'][0]
                    if isinstance(record, dict) and 'fields' in record:
                        fields = record['fields']
                        if 'ID' in fields:
                            record_id = fields['ID']
                            st.success(f"📋 ID Column Value (from response): {record_id}")
                            return record_id
                        elif 'id' in fields:
                            record_id = fields['id']
                            st.success(f"📋 ID Column Value (from response): {record_id}")
                            return record_id
                        elif 'Id' in fields:
                            record_id = fields['Id']
                            st.success(f"📋 ID Column Value (from response): {record_id}")
                            return record_id
            
            # If response is a list
            elif isinstance(response, list) and len(response) > 0:
                record = response[0]
                if isinstance(record, dict) and 'fields' in record:
                    fields = record['fields']
                    if 'ID' in fields:
                        record_id = fields['ID']
                        st.success(f"📋 ID Column Value (from response): {record_id}")
                        return record_id
                    elif 'id' in fields:
                        record_id = fields['id']
                        st.success(f"📋 ID Column Value (from response): {record_id}")
                        return record_id
                    elif 'Id' in fields:
                        record_id = fields['Id']
                        st.success(f"📋 ID Column Value (from response): {record_id}")
                        return record_id
            
            # If we can't get ID from response, try to read it from the database
            if not record_id:
                st.info("🔄 Record ID alınıyor...")
                try:
                    record_id = get_record_by_host_id(event_data['host_id'])
                    
                    if record_id:
                        st.success(f"📋 ID Column Value (from database): {record_id}")
                        return record_id
                    else:
                        st.error("❌ ID Column Value alınamadı")
                        return None
                except Exception as e:
                    st.error(f"❌ Record ID alınırken hata: {e}")
                    return None
        
        st.error("❌ Kayıt oluşturulamadı")
        return None
        
    except Exception as e:
        st.error(f"❌ Etkinlik kaydedilirken hata oluştu: {e}")
        st.error(f"❌ Hata detayı: {type(e).__name__}")
        return None

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
                record_id = save_event(event_data)
                if record_id:
                    # Clear form
                    st.session_state.event_data = {}
                    
                    # Store the redirect URL in session state
                    redirect_url = f"https://eventfeatures.streamlit.app?event_id={record_id}"
                    st.session_state.redirect_url = redirect_url
                    st.session_state.should_redirect = True
                    
                    # Show success message and redirect link
                    st.success("✅ Etkinlik başarıyla kaydedildi!")
                    st.info(f"📋 Record ID: {record_id}")
                    
                    st.markdown("---")
                    st.markdown("### 🔗 Yönlendirme")
                    st.markdown(f"**Hedef URL:** {redirect_url}")
                    
                    # Create a clickable link
                    st.markdown(f"""
                    <a href="{redirect_url}" target="_blank">
                        <button style="
                            background-color: #4CAF50;
                            border: none;
                            color: white;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 4px;
                        ">
                            🚀 Event Features Sayfasına Git
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    st.info("💡 Yukarıdaki butona tıklayarak Event Features sayfasına gidebilirsiniz.")
                    
                    # Stop execution to prevent form reset
                    st.stop()

if __name__ == "__main__":
    main() 