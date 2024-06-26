from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.html import format_html
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.utils import ImageReader
from datetime import datetime

from .models import Article, Commande, CommandeHistorique, Facture, Membre, Panier, LignePanier, Contact
from .forms import AjouterAuPanierForm


def fromage(request):
    return render(request,"fromage.html")
@login_required
def home(request):
    query = request.GET.get('search', '')  # Obtenir le terme de recherche de la requête GET
    if query:
        liste_articles = Article.objects.filter(title__icontains=query)
    else:
        liste_articles = Article.objects.all()
    
    context = {"liste_articles": liste_articles}
    return render(request, "index.html", context)

def detail(request, id_article):
    article = Article.objects.get(id=id_article)
    category = article.category
    article_en_relation = Article.objects.filter(category=category)[:]

    # Supposons que images_list contient les URL des images que vous voulez afficher en bas de la page
    images_list = ["url_image_1.jpg", "url_image_2.jpg", "url_image_3.jpg"]

    return render(request, 'detail.html', {"article": article, "aer": article_en_relation, "images": images_list})

def liste_commandes(request):
    commandes = Commande.objects.all()
    return render(request, 'liste_commandes.html', {'commandes': commandes})

def formulaire_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        # Créez une nouvelle instance de Contact avec les données du formulaire
        Contact.objects.create(nom=name, email=email, message=message_text)
        return redirect('message_list')  # Rediriger vers la page listant les messages
    return render(request, 'formulaire_contact.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def message_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message_content = request.POST.get('message')

        # Vérifier si le champ message est vide
        if not message_content.strip():
            messages.error(request, "Le message ne peut pas être vide.")
            return redirect('message_list')

        # Créer le message seulement si le champ n'est pas vide
        message = Contact.objects.create(name=name, message=message_content)
        messages.success(request, "Message envoyé avec succès.")
        return redirect('message_list')
    
    messages = Contact.objects.all()
    return render(request, 'message_list.html', {'messages': messages})


def delete_message(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return redirect('message_list')  # Redirection vers la liste des messages en cas de méthode GET
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Vérifier si tous les champs sont remplis
        if not username or not password or not email:
            return render(request, 'register.html', {'error': 'Tous les champs sont obligatoires.'})

        # Vérifier si le nom d'utilisateur est déjà pris
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Nom d’utilisateur déjà pris.'})

        try:
            # Créer l'utilisateur
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Styliser le message de bienvenue avec un design exceptionnel
            subject = 'Bienvenue chez La Petite Chèvre'
            message = format_html('''
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                        <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <div style="text-align: center;">
                                <img src="cid:logo" alt="La Petite Chèvre" style="max-width: 150px; margin-bottom: 20px;">
                            </div>
                            <h1 style="color: #333;">Bienvenue {username}!</h1>
                            <p style="color: #666;">Nous sommes ravis de vous avoir parmi nous à <strong>La Petite Chèvre</strong>. Merci de rejoindre notre communauté. Nous espérons que vous apprécierez nos produits et services.</p>
                            <p style="color: #666;">Si vous avez des questions ou besoin d'assistance, n'hésitez pas à nous contacter.</p>
                            <p style="color: #666;">À bientôt!</p>
                            <div style="text-align: center; margin-top: 30px;">
                                <a href="https://www.lapetitechevre.com" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Visitez notre site</a>
                            </div>
                        </div>
                    </body>
                </html>
            ''', username=username)

            email_message = EmailMessage(subject, message, to=[email])
            email_message.content_subtype = "html"
            email_message.attach_file('blog/templates/logo.jpg', 'image/png')
            email_message.send()

            login(request, user)
            return redirect('fromage')
        except IntegrityError:
            return render(request, 'register.html', {'error': 'Erreur lors de l’enregistrement de l’utilisateur. Veuillez réessayer.'})
        except Exception as e:
            return render(request, 'register.html', {'error': f'Erreur inattendue: {str(e)}'})

    return render(request, 'register.html')
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Styliser le message de bienvenue avec un design exceptionnel
                subject = 'Bienvenue chez La Petite Chèvre'
                message = format_html('''
                    <html>
                        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                            <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                                <div style="text-align: center;">
                                    <img src="cid:logo" alt="La Petite Chèvre" style="max-width: 150px; margin-bottom: 20px;">
                                </div>
                                <h1 style="color: #333;">Bienvenue {username}!</h1>
                                <p style="color: #666;">Nous sommes ravis de vous avoir parmi nous à <strong>La Petite Chèvre</strong>. Merci de rejoindre notre communauté. Nous espérons que vous apprécierez nos produits et services.</p>
                                <p style="color: #666;">Si vous avez des questions ou besoin d'assistance, n'hésitez pas à nous contacter.</p>
                                <p style="color: #666;">À bientôt!</p>
                                <div style="text-align: center; margin-top: 30px;">
                                    <a href="https://www.lapetitechevre.com" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Visitez notre site</a>
                                </div>
                            </div>
                        </body>
                    </html>
                ''', username=username)

                email_message = EmailMessage(subject, message, to=[user.email])
                email_message.content_subtype = "html"
                email_message.attach_file('blog/templates/logo.jpg', 'image/png')
                email_message.send()

                return redirect('fromage')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Nom d’utilisateur ou mot de passe incorrect.'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Formulaire invalide. Veuillez réessayer.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.core.mail import EmailMessage
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def custom_logout(request):
    # Styliser le message d'adieu avec un design exceptionnel
    subject = 'Au revoir de chez La Petite Chèvre'
    message = format_html('''
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center;">
                        <img src="cid:logo" alt="La Petite Chèvre" style="max-width: 150px; margin-bottom: 20px;">
                    </div>
                    <h1 style="color: #333;">Au revoir {username}!</h1>
                    <p style="color: #666;">Nous espérons vous revoir bientôt chez <strong>La Petite Chèvre</strong>. Merci pour votre visite et votre fidélité. Nous sommes impatients de vous accueillir à nouveau.</p>
                    <p style="color: #666;">Si vous avez des questions ou besoin d'assistance, n'hésitez pas à nous contacter.</p>
                    <p style="color: #666;">À bientôt!</p>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://www.lapetitechevre.com" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Visitez notre site</a>
                    </div>
                </div>
            </body>
        </html>
    ''', username=request.user.username)

    try:
        email_message = EmailMessage(subject, message, to=[request.user.email])
        email_message.content_subtype = "html"
        email_message.attach_file('blog/templates/logo.jpg', 'image/png')
        email_message.send()
    except Exception as e:
        # Enregistrez l'erreur ou prenez les mesures nécessaires
        print(f'Erreur lors de l\'envoi de l\'email : {e}')

    logout(request)
    return redirect('fromage')

@login_required
def acheter_article(request, id_article):
    if request.method == 'POST':
        article = Article.objects.get(id=id_article)
        nom_client = request.POST.get('nom_client')
        quantite = int(request.POST.get('quantite'))
        modes_paiement = request.POST.get('modes_paiement')
        numero_telephone = request.POST.get('numero_telephone')
        adresse = request.POST.get('adresse')

        # Vérifier que le mode de paiement est sélectionné
        if not modes_paiement:
            return render(request, 'acheter_article.html', {'article': article, 'erreur': 'Veuillez sélectionner un mode de paiement'})

        # Vérifier si la quantité demandée est disponible en stock
        if quantite > article.stock:
            return render(request, 'stock_insuffisant.html', {'article': article, 'erreur': 'La quantité demandée dépasse le stock disponible'})

        # Créer une nouvelle commande dans la base de données
        nouvelle_commande = Commande.objects.create(
            nom_client=nom_client,
            produit=article.title,
            quantite=quantite,
            prix_unitaire=article.prix,
            total=article.prix * quantite,
            modes_paiement=modes_paiement,
            numero_telephone=numero_telephone,
            adresse=adresse
        )

        # Décrémentez le stock après l'achat
        article.stock -= quantite
        article.save()

        # Ajouter la commande confirmée à l'historique des commandes
        CommandeHistorique.objects.create(
            user=request.user,
            produit=article,
            quantite=quantite,
            prix_unitaire=article.prix,
            total=article.prix * quantite
        )

        # Envoyer un email de validation à l'utilisateur connecté
        user_email = request.user.email
        send_validation_email(user_email, article.title, quantite, nouvelle_commande.total)

        # Redirection vers la page de confirmation d'achat avec les données de la commande
        return render(request, 'achat_reussie.html', {'commande': nouvelle_commande})

    else:
        article = Article.objects.get(id=id_article)
        return render(request, 'acheter_article.html', {'article': article})

def send_validation_email(user_email, produit, quantite, total):
    subject = 'Validation de Commande'
    message = format_html('''
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center;">
                        <img src="cid:logo" alt="La Petite Chèvre" style="max-width: 150px; margin-bottom: 20px;">
                    </div>
                    <h1 style="color: #333;">Votre commande a été validée!</h1>
                    <p style="color: #666;">Nous avons le plaisir de vous informer que votre commande pour <strong>{quantite}</strong> unité(s) de <strong>{produit}</strong> a été validée avec succès.</p>
                    <p style="color: #666;">Le montant total de votre commande est de <strong>{total} CFA</strong>.</p>
                    <p style="color: #666;">Merci de votre confiance et à bientôt chez <strong>La Petite Chèvre</strong>.</p>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://www.lapetitechevre.com" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Visitez notre site</a>
                    </div>
                </div>
            </body>
        </html>
    ''', quantite=quantite, produit=produit, total=total)

    email_message = EmailMessage(subject, message, to=[user_email])
    email_message.content_subtype = "html"
    email_message.attach_file('blog/templates/logo.jpg', 'image/png')
    email_message.send()


@login_required
def historique_commandes(request):
    commandes = CommandeHistorique.objects.filter(user=request.user).order_by('-date_commande')
    return render(request, 'historique_commandes.html', {'commandes': commandes})

def confirmation_achat(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    context = {
        'commande': {
            'nom_client': commande.nom_client,
            'produit': commande.produit,
            'quantite': commande.quantite,
            'prix_unitaire': commande.prix_unitaire,
            'total': commande.total,  # Utilisez directement le champ total si déjà calculé
            'modes_paiement': commande.modes_paiement,
            'numero_telephone': commande.numero_telephone,
            'adresse': commande.adresse,
        }
    }
    return render(request, 'confirmation_achat.html', context)

@login_required
def telecharger_facture(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    # Récupérer les données de la commande pour la facture
    nom_client = commande.nom_client
    produit = commande.produit
    quantite = commande.quantite
    prix_unitaire = commande.prix_unitaire
    total = commande.total
    numero_telephone = commande.numero_telephone
    adresse = commande.adresse

    # Date de la commande
    date_commande = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Créer le PDF avec ReportLab
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#003366")
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=12,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#333333"),
        spaceAfter=10
    )

    # Ajouter le logo
    logo_path = "blog/templates/logo.jpg"  # Remplacez par le chemin réel vers votre logo
    logo = Image(logo_path, 1.5 * inch, 1.5 * inch)
    elements.append(logo)

    # Titre de la facture
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("Facture d'Achat", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Détails de la commande
    elements.append(Paragraph(f"Date de la commande: {date_commande}", body_style))
    elements.append(Paragraph(f"Nom du Client: {nom_client}", body_style))
    elements.append(Paragraph(f"Adresse: {adresse}", body_style))
    elements.append(Paragraph(f"Numéro de téléphone: {numero_telephone}", body_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Création du tableau des articles
    data = [['Produit', 'Quantité', 'Prix Unitaire (FCFA)', 'Total (FCFA)']]
    data.append([produit, str(quantite), str(prix_unitaire), str(total)])

    # Ajout de la ligne du total
    data.append(['', '', 'Total', total])

    # Création et style du tableau
    table = Table(data, colWidths=[2.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    
    elements.append(table)
    
    # Ajout du message de remerciement avec le nom de l'utilisateur
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Merci pour votre achat, {request.user.username}! Nous vous remercions de votre confiance.", body_style))
    
    # Générer le PDF
    pdf.build(elements)
    buffer.seek(0)

    # Enregistrer la facture dans la base de données
    facture = Facture.objects.create(
        commande=commande,
        contenu_pdf=buffer.getvalue(),
        nom_client=nom_client,
        adresse=adresse,
        quantite=quantite,
        prix_unitaire=prix_unitaire,
        total=total,
        numero_telephone=numero_telephone,
        modes_paiement=commande.modes_paiement
    )

    # Envoyer la facture par e-mail à l'utilisateur connecté
    subject = 'Votre facture'
    message = 'Veuillez trouver ci-joint votre facture.'
    from_email = 'votre_email@gmail.com'  # Remplacez par votre adresse e-mail
    recipient_email = request.user.email  # Utilisez l'email de l'utilisateur connecté

    email = EmailMessage(subject, message, from_email, [recipient_email])
    email.attach(f'facture_{commande_id}.pdf', buffer.getvalue(), 'application/pdf')
    email.send()

    # Réponse HTTP avec le contenu du PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{commande_id}.pdf"'
    response.write(buffer.getvalue())

    return response




def achat_reussie(request, commande_id):
    # Récupérer la commande à partir de l'ID
    commande = Commande.objects.get(id=commande_id)
    return render(request, 'achat_reussie.html', {'commande': commande})

@login_required
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        # Supprimer la commande de la base de données
        commande.delete()
        
        # Envoyer un email de confirmation d'annulation à l'utilisateur
        user_email = request.user.email
        subject = 'Annulation de commande'
        message = format_html('''
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                        <div style="text-align: center;">
                            <img src="cid:logo" alt="La Petite Chèvre" style="max-width: 150px; margin-bottom: 20px;">
                        </div>
                        <h1 style="color: #333;">Annulation de commande</h1>
                        <p style="color: #666;">Votre commande <strong>{commande_id}</strong> a été annulée avec succès.</p>
                        <p style="color: #666;">Merci de votre compréhension. Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter.</p>
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="https://www.lapetitechevre.com" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Visitez notre site</a>
                        </div>
                    </div>
                </body>
            </html>
        ''', commande_id=commande_id)

        email = EmailMessage(subject, message, to=[user_email])
        email.content_subtype = "html"
        email.attach_file('blog/templates/logo.jpg', 'image/png')
        email.send()
        
        # Rediriger vers une page de confirmation d'annulation ou une autre page appropriée
        return redirect('annulation_reussie')
    # Si la méthode n'est pas POST, afficher la page de confirmation
    return render(request, 'annuler_commande.html', {'commande': commande})

def annulation_reussie(request):
    return render(request, 'annulation_reussie.html')

def connexion_reussie(request):
    return render(request, 'connexion_reussie.html')

def entreprise(request):
    # Logique de vue pour la page d'entreprise
    return render(request, 'entreprise.html')
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Panier, LignePanier

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Article, Panier, LignePanier

@login_required
@require_POST
def ajouter_au_panier(request, id_article):
    article = get_object_or_404(Article, id=id_article)
    user_panier, created = Panier.objects.get_or_create(user=request.user)
    quantite = int(request.POST.get('quantite', 1))  # Obtenir la quantité du formulaire, par défaut 1
    if quantite <= article.stock:  # Vérifiez si la quantité demandée est disponible en stock
        try:
            ligne_panier = LignePanier.objects.get(panier=user_panier, article=article)
            ligne_panier.quantite += quantite
            ligne_panier.save()  # Sauvegarde de la ligne de panier modifiée
        except LignePanier.DoesNotExist:
            LignePanier.objects.create(
                panier=user_panier,
                article=article,
                quantite=quantite,
                prix_unitaire=article.prix
            )  # Création d'une nouvelle ligne de panier si elle n'existe pas
        # Décrémentez le stock après l'ajout au panier
        article.stock -= quantite
        article.save()
        return HttpResponse(status=204)  # Réponse vide sans contenu ni message
    else:
        return render(request, 'stock_insuffisant.html')  # Afficher la page de stock insuffisant



from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import LignePanier

@login_required
def modifier_quantite_panier(request, id_ligne):
    if request.method == 'POST':
        ligne_panier = get_object_or_404(LignePanier, id=id_ligne)
        if ligne_panier.panier.user == request.user:
            nouvelle_quantite = int(request.POST.get('nouvelle_quantite', 1))
            if nouvelle_quantite > 0:
                ligne_panier.quantite = nouvelle_quantite
                ligne_panier.save()
                return redirect('panier')
    return HttpResponseBadRequest('Erreur lors de la modification de la quantité.')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Panier, LignePanier

def panier(request):
    user = request.user
    try:
        user_panier = Panier.objects.get(user=user)
    except Panier.DoesNotExist:
        user_panier = None
    
    lignes_panier = LignePanier.objects.filter(panier=user_panier) if user_panier else []
    total_prix = sum(ligne.prix_total for ligne in lignes_panier)
    
    if request.method == 'POST' and 'commander' in request.POST:
        return redirect('panier_validez')
    
    return render(request, 'panier.html', {'lignes_panier': lignes_panier, 'total_prix': total_prix})


def supprimer_panier(request, id_ligne):
    ligne_panier = get_object_or_404(LignePanier, id=id_ligne)
    if ligne_panier.panier.user == request.user:
        ligne_panier.delete()
    return redirect('panier')


@login_required
def telechargez_facture(request, contenu_panier, total_prix):
    # Créer le PDF de la facture
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=12,
        alignment=TA_CENTER
    )

    # Ajouter le logo
    logo_path = "blog/templates/logo.jpg"  # Remplacez par le chemin réel vers votre logo
    logo = Image(logo_path, 2 * inch, 2 * inch)
    logo.hAlign = 'CENTER'
    elements.append(logo)

    # Titre de la facture
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Facture d'Achat", title_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Création du tableau des articles
    data = [['Article', 'Quantité', 'Prix Unitaire (FCFA)', 'Prix Total (FCFA)']]
    for item in contenu_panier:
        data.append([str(item['article']), item['quantite'], item['prix_unitaire'], item['prix_total']])
    
    # Ajout de la ligne du total
    data.append(['', '', 'Total', total_prix])

    # Création et style du tableau
    table = Table(data, colWidths=[2 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    
    elements.append(table)
    
    # Ajout du message de remerciement avec le nom de l'utilisateur
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"Merci pour votre achat, {request.user.username}! Nous vous remercions de votre confiance.", body_style))
    
    # Ajouter une page de séparation avec un message de remerciement
    elements.append(PageBreak())
    elements.append(Paragraph("Nous espérons vous revoir bientôt!", title_style))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("La Petite Chèvre vous remercie.", body_style))
    
    # Générer le PDF
    pdf.build(elements)
    buffer.seek(0)

    # Envoyer la facture par e-mail
    user_email = request.user.email
    subject = 'Facture d\'Achat'
    message = 'Votre facture d\'achat est jointe à cet e-mail. Merci pour votre confiance.'
    email = EmailMessage(subject, message, to=[user_email])
    email.attach('facture.pdf', buffer.getvalue(), 'application/pdf')
    email.send()

    # Télécharger la facture comme réponse HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="facture.pdf"'
    response.write(buffer.getvalue())

    return response

@login_required
def confirmation_achat_panier(request):
    user_panier = get_object_or_404(Panier, user=request.user)
    lignes_panier = LignePanier.objects.filter(panier=user_panier)

    contenu_panier = [{'article': ligne.article, 'quantite': ligne.quantite, 'prix_unitaire': ligne.article.prix, 'prix_total': ligne.prix_total} for ligne in lignes_panier]
    total_prix = sum(ligne.prix_total for ligne in lignes_panier)
    
    # Appel de la vue pour générer et télécharger la facture
    return telechargez_facture(request, contenu_panier, total_prix)

@login_required
def panier_validez(request):
    # Envoyer un e-mail de confirmation de commande à l'utilisateur connecté
    subject = 'Validation de Commande'
    message = format_html('''
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center;">
                        <img src="cid:logo" alt="La Petite Chèvre" style="max-width: 150px; margin-bottom: 20px;">
                    </div>
                    <h1 style="color: #333;">Votre commande a été validée!</h1>
                    <p style="color: #666;">Nous avons le plaisir de vous informer que votre achat sur <strong>La Petite Chèvre</strong> a été effectué avec succès.</p>
                    <p style="color: #666;">Merci de votre confiance et à bientôt chez <strong>La Petite Chèvre</strong>.</p>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://www.lapetitechevre.com" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Visitez notre site</a>
                    </div>
                </div>
            </body>
        </html>
    ''')

    from_email = 'votre_adresse_email@example.com'  # Remplacez par votre adresse email
    user_email = request.user.email  # Récupérer l'email de l'utilisateur connecté
    
    email = EmailMessage(subject, message, from_email, [user_email])
    email.content_subtype = "html"
    email.attach_file('blog/templates/logo.jpg', 'image/png')  # Remplacez par le chemin correct vers le logo de votre entreprise
    email.send()
    
    return render(request, 'panier_validez.html')
def membres(request):
    membres = Membre.objects.all()
    context = {'membres': membres}
    return render(request, 'membres.html', context)
from django.shortcuts import render

def stock_insuffisant(request):
    return render(request, 'stock_insuffisant.html')


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

