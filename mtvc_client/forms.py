import datetime

from django import forms
from django.core.exceptions import ValidationError

import utils


def validate_year_of_birth(value):
    if value < 1900 or value > datetime.date.today().year:
        raise ValidationError('Not a valid year: %s' % value)


def validate_accepted_tc(value):
    if not value:
        raise ValidationError('Terms and Conditions must be accepted')


class ProfileForm(forms.Form):
    product = forms.ChoiceField(
        label='Package',
        choices=utils.get_product_choices(),
        initial='',
        required=False)
    is_trial = forms.BooleanField(widget=forms.HiddenInput())
    gender = forms.ChoiceField(
        label='Gender',
        choices=utils.get_gender_choices(),
        initial='')
    year_of_birth = forms.IntegerField(
        label='Year of birth',
        initial=None,
        validators=[validate_year_of_birth])
    region = forms.ChoiceField(
        label='Region',
        choices=utils.get_region_choices(),
        initial='')
    have_dstv_at_home = forms.ChoiceField(
        help_text='Do you have DSTV at home?',
        label='Do you have DSTV at home?',
        choices=(('', '---------'), (True, 'Yes'), (False, 'No')),
        initial='')
    accepted_tc = forms.BooleanField(
        label='Accept terms & conditions',
        validators=[validate_accepted_tc])


class ProductForm(forms.Form):
    product = forms.ChoiceField(
        label='Package',
        choices=utils.get_product_choices(),
        initial='')
