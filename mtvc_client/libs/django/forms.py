import datetime
import json

from django import forms
from django.utils.functional import lazy
from django.core.exceptions import ValidationError
from django.forms.widgets import RadioFieldRenderer, mark_safe, RadioInput, \
    conditional_escape
from django.utils.encoding import force_text

from mtvc_client.libs.django import utils


def validate_year_of_birth(value):
    if value < (datetime.date.today().year - 100) or \
            value > datetime.date.today().year:
        raise ValidationError('Not a valid year: %s' % value)


def validate_accepted_tc(value):
    if not value:
        raise ValidationError('Terms and Conditions must be accepted')


class RadioInputNoLabel(RadioInput):
    """
    An object used by RadioFieldBreakRenderer that represents a single
    <input type='radio'>, but without the label that Django
    automatically prefixes during rendering
    """

    def __unicode__(self):
        choice_label = conditional_escape(force_text(self.choice_label))
        return mark_safe(u'%s %s' % (self.tag(), choice_label))


class RadioFieldParagraphRenderer(RadioFieldRenderer):
    """
    Overrides rendering of the object used by RadioSelect to wrap
    choices in html paragraph-tags (<p></p>) instead of the lu-li option
    that Django offers by default
    """

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RadioInputNoLabel(
                self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]  # let IndexErrors propagate
        return RadioInputNoLabel(
            self.name, self.value, self.attrs.copy(), choice, idx)

    def render(self):
        """
        Outputs radio fields wrapped in p-tags.
        """
        return mark_safe(u'\n'.join([
            u'<p>%s</p>' % force_text(w) for w in self]))


class JSONDataForm(forms.Form):

    def get_json_data(self):
        return json.dumps(self.cleaned_data)


class ProfileForm(JSONDataForm):
    product = forms.ChoiceField(
        label='Package',
        choices=lazy(utils.get_product_choices, list)(),
        initial='',
        required=False,
        widget=forms.RadioSelect(renderer=RadioFieldParagraphRenderer))
    is_trial = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    gender = forms.ChoiceField(
        label='Gender',
        choices=lazy(utils.get_gender_choices, list)(),
        initial='')
    year_of_birth = forms.TypedChoiceField(
        label='Year of birth',
        coerce=int,
        validators=[validate_year_of_birth],
        choices=[('', '---------')] + [(i, i) for i in reversed(range(
            datetime.date.today().year - 100, datetime.date.today().year))])
    region = forms.ChoiceField(
        label='Region',
        choices=lazy(utils.get_region_choices, list)(),
        initial='')
    dstv_at_home = forms.ChoiceField(
        help_text='Do you have DSTV at home?',
        label='Do you have DSTV at home?',
        choices=(('', '---------'), (True, 'Yes'), (False, 'No')),
        initial='')
    accepted_tc = forms.BooleanField(
        label='Accept terms & conditions',
        validators=[validate_accepted_tc])


class ProductForm(JSONDataForm):
    product = forms.ChoiceField(
        label='Package',
        choices=lazy(utils.get_product_choices, list)(),
        initial='',
        widget=forms.RadioSelect(renderer=RadioFieldParagraphRenderer))
