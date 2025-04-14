import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice, randint

import django
from django.conf import settings

# --- Configuração Django ---
DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
settings.USE_TZ = False

django.setup()
# --- Fim Configuração Django ---

# --- Imports dos Models (depois do setup) ---
# Colocar fora do if __name__ para clareza, já que o setup está fora também
# Ou manter tudo dentro do if, mas importar models depois do setup.
# A organização atual funciona.
# --- Fim Imports Models ---


if __name__ == "__main__":
    import faker
    from contact.models import Category, Contact

    # É importante importar faker e models AQUI se o setup estiver fora do if

    print("Deleting existing Categories and Contacts...")
    # Ordem sugerida: deletar categorias primeiro
    Category.objects.all().delete()
    Contact.objects.all().delete()
    print("Deletion complete.")

    fake = faker.Faker("pt_BR")

    print("Creating Categories...")
    category_names = [
        "Amigos",
        "Família",
        "Conhecidos",
    ]
    django_categories_instances = [Category(name=name) for name in category_names]
    # Usar bulk_create aqui também
    Category.objects.bulk_create(django_categories_instances)
    print(f"{len(category_names)} Categories created.")

    # Buscar as categorias que *realmente* existem no banco agora
    # Isso garante que estamos usando objetos com PKs válidos
    # Converte para lista para uso com choice
    categories_from_db = list(Category.objects.all())

    if not categories_from_db:
        print("Error: No categories found in the database after creation. Exiting.")
        sys.exit(1)  # Sai se não conseguiu criar/encontrar categorias

    print(f"Creating {NUMBER_OF_OBJECTS} Contacts...")
    django_contacts = []
    for i in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()
        email = profile["mail"]
        # Adicionar um pequeno número ao email para aumentar a chance de ser único
        # numa execução com menos de 1000, se faker repetir emails.
        email_parts = email.split("@")
        email = f"{email_parts[0]}{i}@{email_parts[1]}"

        first_name, last_name = profile["name"].split(" ", 1)
        phone = fake.phone_number()
        created_date: datetime = fake.date_this_year()
        description = fake.text(max_nb_chars=100)

        # *** CORREÇÃO PRINCIPAL: Escolher da lista buscada do DB ***
        category = choice(categories_from_db)

        django_contacts.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                created_date=created_date,
                description=description,
                category=category,
                owner=None,
            )
        )
        if (i + 1) % 100 == 0:  # Feedback a cada 100 contatos
            print(f"  Prepared {i + 1}/{NUMBER_OF_OBJECTS} contacts...")

    if len(django_contacts) > 0:
        print(f"Bulk creating {len(django_contacts)} contacts...")
        Contact.objects.bulk_create(django_contacts)
        print("Contacts creation complete.")
    else:
        print("No contacts generated.")
