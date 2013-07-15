from webtest.form import Form, Field as WebTestField

def add_extra_form_to_formset_with_data(form, prefix, field_names_and_values):
    total_forms_field_name = prefix + '-TOTAL_FORMS'
    next_form_index = int(form[total_forms_field_name].value)
    for extra_field_name, extra_field_value in field_names_and_values.iteritems():
        input_field_name = '-'.join((prefix, str(next_form_index), extra_field_name))
        extra_field = WebTestField(form, tag='input', name=input_field_name, pos=0, value=extra_field_value)
        form.fields[input_field_name] = [extra_field]
        form[input_field_name] = extra_field_value
        form.field_order.append((input_field_name, extra_field))
        form[total_forms_field_name].value = str(next_form_index + 1)

Form.add_extra_form_to_formset_with_data = add_extra_form_to_formset_with_data
