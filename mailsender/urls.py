from django.urls import path
from mailsender.apps import MailsenderConfig
from mailsender.views import *

app_name = MailsenderConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients/', ClientManagementListView.as_view(), name='clients_list'),
    path('clients/new/', ClientManagementCreateView.as_view(), name='client_form'),
    path('clients/<int:pk>/', ClientManagementDetailView.as_view(), name='client_detail'),
    path('clients/update/<int:pk>/', ClientManagementUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientManagementDeleteView.as_view(), name='client_confirm_delete'),

    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('messages/new/', MessageCreateView.as_view(), name='message_form'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_confirm_delete'),

    path('mailings/', MailingListView.as_view(), name='mailings_list'),
    path('mailings/new/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_confirm_delete'),

    path('mailings/<int:pk>/send/', MailingSendView.as_view(), name='send_mailing'),

    path('mailings/<int:mailing_id>/attempts/', MailingAttemptListView.as_view(), name='mailing_attempts'),
]
