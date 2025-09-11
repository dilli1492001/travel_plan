from fastapi import APIRouter, Cookie, Request, Form
from fastapi.templating import Jinja2Templates
from streamlit import user
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse


from src.integrations.resend import send_email
from src.integrations.openai import generate_plan
from src.config.db import db
from utils import get_loggedin_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get('/')
def home():
    return RedirectResponse('/signup')

@router.get('/signup')
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {'request': request})

@router.post('/api/signup')
def api_signup(request: Request, email = Form(...), password = Form(...)):
    result = db.auth.sign_up({
        'email': email,
        'password': password
    })

    if result.user:
        return JSONResponse({
            'message': 'User Created successfully',
            'token': result.session.access_token
        })




@router.get('/login')
def login(request: Request):
    return templates.TemplateResponse("login.html", {'request': request})


@router.get('/logout')
def logout(request: Request):
    res=RedirectResponse('/login',status_code=302)
    res.delete_cookie('user_session')
    res.delete_cookie('refresh_token')
    return res
    


@router.post('/api/login')
def api_login(request: Request, email = Form(...), password = Form(...)):
    try:
        result = db.auth.sign_in_with_password({
            'email': email,
            'password': password
            })

        if result.user:
            response = RedirectResponse('/dashboard',status_code=302)
            response.set_cookie("user_session", result.session.access_token, max_age=3600)
            return response
    except Exception as e :
        return templates.TemplateResponse("login.html", {'request': request,"msg":str(e)})




@router.get('/dashboard') 
def dashboard(request:Request):
    # user = get_loggedin_user(request)
    # if user:
    #     return templates.TemplateResponse('dashboard.html',{'request':request})
    # return RedirectResponse('/login')
    user = get_loggedin_user(request)
    if user:
        result = db.table('travel_plans').select('*').eq('user_id', user.id).execute()
        print(result.data)
        return templates.TemplateResponse('dashboard.html', {'request': request, 'plans': result.data})
    return RedirectResponse('/login')
    



@router.get('/plans/new') 
def new_plan(request:Request):
    user = get_loggedin_user(request)
    if user:
        return  templates.TemplateResponse('new_plan.html',{'request':request})
    return RedirectResponse('/login')




@router.post('/plans/new') 
def create_plan(
    request:Request,
    title:str=Form(...),
    days:int=Form(...),
    persons:int=Form(...),
    budget:str=Form(...),
    city:str=Form(...)
    ):
    user = get_loggedin_user(request)
    if user:
        result=db.table('travel_plans').insert({
            'user_id':user.id,
            'title':title,
            'days':days,
            'budget':budget,
            'cities':city,
            'persons_count':persons,
            'ai_plan':"Nothing..."
        }).execute()

        if result.data:
             return RedirectResponse(f'http://127.0.0.1:8000/plans/generate?plan_id={result.data[0]["id"]}', status_code=302)





@router.get('/plans/generate') 
def create_plan(request:Request,plan_id):
    print(plan_id)

    result=db.table('travel_plans').select('*').eq('id',plan_id).execute()

    if result.data:
        plan=generate_plan(str(result.data[0]))

        result1=db.table('travel_plans').update({
            'ai_plan':plan
        }).eq('id',plan_id).execute()

    if result1.data:
        return templates.TemplateResponse("new_plan_edit.html", {
               'request': request, 
               'plan': result1.data[0]
            })
       




@router.post('/plans/save') 
def save_plan(request:Request,plan_id=Form(...),planContent=Form(...)):

    user = get_loggedin_user(request)
    if user:
        result = db.table('travel_plans').update({
            'ai_plan':planContent
        }).eq('id',plan_id).execute()

        plan=result.data[0]

        send_email(user.email,plan['ai_plan'],plan['cities'])

        if result.data:
            return RedirectResponse('/dashboard',status_code=302)
    


@router.get('/plans/edit/{plan_id}') 
def edit_plan(request:Request,plan_id):
    user = get_loggedin_user(request)
    if user:
        result = db.table('travel_plans').select('*').eq('id',plan_id).execute()
        if result.data:
            return templates.TemplateResponse('new_plan_edit.html',{'request':request, 'plan':result.data[0]})
        



@router.get('/plans/delete/{plan_id}') 
def delete_plan(request:Request,plan_id):
    user = get_loggedin_user(request)
    if user:
        res =db.table('travel_plans').delete().eq('id',plan_id).execute()
        return RedirectResponse('/dashboard',status_code=302)
    


      

