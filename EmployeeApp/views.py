from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmployeeApp.models import Departments,Employees
from EmployeeApp.serializers import DepartmentSerializer,EmployeeSerializer

from django.core.files.storage import default_storage

# Create your views here.
# Add API method for Departments
@csrf_exempt
def departmentApi(request,id=0):
    if request.method=='GET':
        if id != 0:
            try:
                department = Departments.objects.get(DepartmentId=id)
                department_serializer = DepartmentSerializer(department)
                specific_department = department_serializer.data
                return JsonResponse({'data': specific_department, 'message': 'Fetched Successfully!!', 'statusCode': 200}, safe=False)
            except Departments.DoesNotExist:
                return JsonResponse({'error': 'Department not found'}, status=404)
        else:
            departments = Departments.objects.all()
            departments_serializer = DepartmentSerializer(departments, many=True)
            return JsonResponse(departments_serializer.data, safe=False)
    elif request.method=='POST':
        department_data = JSONParser().parse(request)
        department_serializer = DepartmentSerializer(data=department_data)
        print(department_serializer, 'department_serializer')
        if department_serializer.is_valid():
            department_serializer.save()
            new_department_data = department_serializer.data
            return JsonResponse({'data': new_department_data, 'message': 'Added Successfully!!', 'statusCode': 201}, status=201)  # Return serialized data with status code 201 (Created)
        return JsonResponse(department_serializer.errors, status=400)
    elif request.method=='PUT':
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        department_serializer=DepartmentSerializer(department,data=department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update,", safe=False)
    elif request.method=='DELETE':
        department = Departments.objects.get(DepartmentId=id)
        deleted_department_id = department.DepartmentId
        department.delete()
        return JsonResponse({'message': 'Deleted Successfully!!', 'DepartmentId': str(deleted_department_id), 'statusCode': 200}, status=200)
    

# Add API method for Employees
@csrf_exempt
def employeeApi(request,id=0):
    if request.method=='GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data, safe=False)
    elif request.method=='POST':
        employee_data = JSONParser().parse(request)
        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse("Failed to Add.", safe=False)
    elif request.method=='PUT':
        employee_data = JSONParser().parse(request)
        employee = Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
        employee_serializer=EmployeeSerializer(employee,data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update,", safe=False)
    elif request.method=='DELETE':
        employee = Employees.objects.get(EmployeeId=id)
        employee.delete()
        return JsonResponse("Deleted Successfully!!", safe=False)
    
@csrf_exempt
def SaveFile(request):
    file = request.FILES['uploadedFile']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)