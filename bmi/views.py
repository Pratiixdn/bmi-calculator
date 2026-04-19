from django.shortcuts import render


def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return {
            'label': 'Underweight',
            'color': '#60a5fa',
            'icon': '↓',
            'advice': 'Consider a nutrient-rich diet with healthy caloric surplus. Consult a healthcare provider.',
            'risk': 'Low',
        }
    elif bmi < 25:
        return {
            'label': 'Normal Weight',
            'color': '#34d399',
            'icon': '✓',
            'advice': 'Great work! Maintain your healthy lifestyle with balanced diet and regular exercise.',
            'risk': 'Minimal',
        }
    elif bmi < 30:
        return {
            'label': 'Overweight',
            'color': '#fbbf24',
            'icon': '△',
            'advice': 'Moderate changes in diet and increased physical activity can help. Consult a doctor.',
            'risk': 'Increased',
        }
    else:
        return {
            'label': 'Obese',
            'color': '#f87171',
            'icon': '!',
            'advice': 'Please consult a healthcare professional for a personalized weight management plan.',
            'risk': 'High',
        }


def bmi_view(request):
    context = {}

    if request.method == 'POST':
        try:
            unit_system = request.POST.get('unit_system', 'metric')
            age = int(request.POST.get('age', 0))
            gender = request.POST.get('gender', '')

            if unit_system == 'metric':
                weight = float(request.POST.get('weight_kg', 0))
                height = float(request.POST.get('height_cm', 0))
            else:
                weight_lbs = float(request.POST.get('weight_lbs', 0))
                feet = float(request.POST.get('height_ft', 0))
                inches = float(request.POST.get('height_in', 0))
                weight = weight_lbs * 0.453592
                height = (feet * 30.48) + (inches * 2.54)

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive.")

            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)

            # Healthy weight range for user's height
            healthy_min = round(18.5 * (height / 100) ** 2, 1)
            healthy_max = round(24.9 * (height / 100) ** 2, 1)

            context = {
                'bmi': bmi,
                'category': category,
                'weight_kg': round(weight, 1),
                'height_cm': round(height, 1),
                'age': age,
                'gender': gender,
                'healthy_min': healthy_min,
                'healthy_max': healthy_max,
                'unit_system': unit_system,
                'gauge_pct': min(max((bmi - 10) / (45 - 10) * 100, 0), 100),
            'gauge_rotation': round(min(max((bmi - 10) / (45 - 10), 0), 1) * 180 - 90, 1),
            }

        except (ValueError, ZeroDivisionError) as e:
            context['error'] = 'Please enter valid positive numbers for all fields.'

    return render(request, 'bmi/index.html', context)
