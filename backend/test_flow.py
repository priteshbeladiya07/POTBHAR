import urllib.request
import urllib.parse
import json

BASE = 'http://127.0.0.1:8000/api/v1'

def post_form(url, data):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

def post_json(url, data, token=None):
    body = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

def get_json(url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

# 1. Login Donor
login_res = post_form(f'{BASE}/auth/login', {'username': 'donor@potbhar.demo', 'password': 'demo123'})
donor_token = login_res['access_token']
print('[1] Donor Login OK! Token acquired.')

# 2. Get Me
me = get_json(f'{BASE}/auth/me', donor_token)
print(f"[2] Auth Me OK: {me['full_name']} ({me['role']}) - Org: {me['organization']['name']}")

from datetime import datetime

# 3. Create Food Batch
batch = post_json(f'{BASE}/food-batches/', {
    'food_category': 'Biryani',
    'description': 'Surplus fresh vegetable biryani from lunch banquet',
    'quantity_kg': 25.0,
    'preparation_time': datetime.utcnow().isoformat(),
    'storage_temp': 'ROOM_TEMP',
    'storage_method': 'SEALED',
    'packaging_intact': True,
    'handling_completeness': 0.9,
    'transport_duration_hours': 0.5
}, donor_token)
batch_id = batch['id']
print(f"[3] Food Batch Created OK: {batch_id} - {batch['food_category']} {batch['quantity_kg']}kg (Status: {batch['status']})")

# 4. Assess Risk with FreshGuard AI
risk = post_json(f'{BASE}/food-batches/{batch_id}/assess-risk', {}, donor_token)
print(f"[4] FreshGuard Risk OK: Category={risk.get('risk_category')}, Flags={len(risk.get('risk_flags', []))}, RequiresReview={risk.get('requires_assessor_review')}")

# 5. Submit Batch
submit_res = post_json(f'{BASE}/food-batches/{batch_id}/submit', {}, donor_token)
print(f"[5] Batch Submitted OK: Status={submit_res['status']}")

# 6. Login Assessor
assessor_login = post_form(f'{BASE}/auth/login', {'username': 'assessor@potbhar.demo', 'password': 'demo123'})
assessor_token = assessor_login['access_token']
print('[6] Assessor Login OK!')

# 7. Assessor Approves Batch
approval = post_json(f'{BASE}/food-batches/{batch_id}/approve', {
    'decision': 'APPROVED',
    'reason': 'Quality verified: packaging intact, safe temperature and handling parameters met.'
}, assessor_token)
print(f"[7] Assessor Approved OK: Status={approval['status']}")

# 8. Run Matching Engine
match_run = post_json(f'{BASE}/matches/run-matching/{batch_id}', {}, assessor_token)
print(f"[8] Match Engine Run OK: {match_run}")

# 9. List Matches
matches = get_json(f'{BASE}/matches/', donor_token)
print(f"[9] Total Active Matches: {len(matches)}")

# 10. Report Organic Waste
waste = post_json(f'{BASE}/waste-batches/', {
    'waste_category': 'Vegetable Prep Waste',
    'quantity_kg': 15.0,
    'contamination_status': 'CLEAN',
    'contamination_details': 'Segregated kitchen prep organic trim'
}, donor_token)
print(f"[10] Waste Reported OK: ID={waste['id']} - {waste['quantity_kg']}kg (Status: {waste['status']})")

# 11. Analytics Summary
analytics = get_json(f'{BASE}/analytics/summary', donor_token)
fr = analytics.get('food_recovery', {})
wm = analytics.get('waste_management', {})
print(f"[11] Analytics Summary OK: Meals={fr.get('estimated_meals_served')}, Waste Diverted={wm.get('total_waste_diverted_kg')}kg, Orgs={analytics.get('organizations', {}).get('total')}")
print('\n*** ALL 11 ENDPOINTS TESTED AND 100% OPERATIONAL! ***')
