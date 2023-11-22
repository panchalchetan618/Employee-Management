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


def index(request):
    return render(request, "home/index.html")


class FileView(APIView):
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response(
                    {"status": False, "message": "Please Upload a file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            excel_file = data.get("file")
            df = pd.read_excel(excel_file, sheet_name=0)
            persons = []

            for index, row in df.iterrows():
                emp_id = row["Emp_Id"]
                name = row["Name"]
                salary = row["Salary"]
                designation = row["Ddesignation"]
                address = row["Address"]
                person = Person(
                    emp_id=emp_id,
                    name=name,
                    salary=salary,
                    designation=designation,
                    address=address,
                )
                if not Person.objects.filter(emp_id=person.emp_id).exists():
                    persons.append(person)

            Person.objects.bulk_create(persons)
            return Response(
                {"status": True, "message": "Successfully created"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            error_message = str(e)
            return Response(
                {"status": False, "message": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )


class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False, methods=["GET"])
    def by_name(self, request):
        name = request.query_params.get("name", None)
        if name is not None:
            persons = Person.objects.filter(name__icontains=name)
            serializer = self.get_serializer(persons, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Please provide a name parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
