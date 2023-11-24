from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileSerializer, PersonSerializer
from rest_framework.decorators import action
from .models import Person
import pandas as pd


# Render home page

def index(request):
    return render(request, "home/index.html")


# Upload File View

class FileView(APIView):
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response(
                    {"status": False, "message": "Please Upload a valid file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            excel_file = data.get("file")
            if excel_file is None:
                return Response(
                    {"status": False, "message": "Please Upload a file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            df = pd.read_excel(excel_file, sheet_name=0)
            persons = []

            for index, row in df.iterrows():
                emp_id = row.get("Emp_Id")
                name = row.get("Name")
                salary = row.get("Salary")
                designation = row.get("Designation") or row.get("Ddesignation")
                address = row.get("Address")

                if (
                    emp_id is not None
                    and name is not None
                    and salary is not None
                    and designation is not None
                    and address is not None
                ):
                    person = Person(
                        emp_id=emp_id,
                        name=name,
                        salary=salary,
                        designation=designation,
                        address=address,
                    )
                    if not Person.objects.filter(emp_id=person.emp_id).exists():
                        persons.append(person)

                else:
                    return Response(
                        {"status": False, "message": "Please Upload a valid file"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            Person.objects.bulk_create(persons)
            return Response(
                {"status": True, "message": "Successfully created"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            error_message = str(e)
            return Response(
                {"status": False, "message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Get person by Name View

class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False, methods=["GET"])
    def by_name(self, request):
        name = request.query_params.get("name", None)
        if name is not None:
            persons = Person.objects.filter(name__icontains=name)
            if persons is not None:
                serializer = self.get_serializer(persons, many=True)
                return Response(serializer.data)
            else:
                return Response(
                {"error": "Person not found"},
                status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Please provide a name parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
