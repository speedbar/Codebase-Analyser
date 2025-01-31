import plotly.graph_objects as go
import pandas as pd

# Load the Excel file
file_path = 'Must Win Deals Data.xlsm'
sheet_name = '20 Sep'

# Read the data from the specified sheet starting from the 4th row
df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)

# Replace these with actual column names
main_key_column = 'MU'  # Assuming MU is the main key
label_column = 'Client'  # Assuming Client is the label
stage_column = 'Stage'  # Assuming Sales Stage Date is the stage
size_column = 'TCV £M'
sizecv_column = 'CV £M' # Updated to include CV £M
opp_column = 'Opp'  # Assuming Opp is the opportunity data
new_deal_column = 'Status' 

# Define the custom order for the stages
stage_order = {'Proactive': 0, '3 - Opportunity Qualification': 1, '4 - Winning Strategy': 2, '5 - Finalising the Solution':3, '6 - Proposing':4,'7 - Formalising Agreement':5}

# Define the stage groups
stage_groups = {
    'group_1': ['Proactive Deal', 'D - Dropped'],
    'group_2': ['3 - Opportunity Qualification'],
    'group_3': ['4 - Winning Strategy','5 - Finalising the Solution','6 - Proposing','7 - Formalising Agreement']
}

def get_stage_group(stage):
    # Clean the stage value
    stage = str(stage).strip()
    for group, stages in stage_groups.items():
        if stage in stages:
            return group
    return 'Others'

# Initialize an empty dictionary to store the final data
data = {}

def get_first_two_words(text):
    words = text.split()
    return ' '.join(words[:2])

# Initialize a counter to track the number of rows processed
row_count = 0

for index, row in df.iterrows():
    row_count += 1
    main_key = str(row[main_key_column])  # Convert main_key to string
    label = row[label_column]
    stage = row[stage_column]
    size = row[size_column]
    sizeCV = row[sizecv_column]
    opp = row[opp_column]  # Pick the "opp" data from the second column
    newdeal = row[new_deal_column]  # Get the "New Deal?" data

    # Print the row for debugging purposes
    print(f"Row {row_count}: {row}")

    if pd.isna(main_key) or pd.isna(label) or pd.isna(stage) or pd.isna(size) or pd.isna(sizeCV) or pd.isna(opp):
        print(f"Skipping row {row_count} due to missing data.")
        continue

    main_key = str(main_key)

    # Correct unwanted data issues
    if isinstance(label, str):
        label = label.replace('\xa0', ' ')
    if isinstance(stage, str):
        stage = stage.replace('\xa0', ' ').strip()
    if isinstance(size, str):
        size = size.replace('-', '0')
    if isinstance(sizeCV, str):
        sizeCV = sizeCV.replace('-', '0')
    if isinstance(main_key, str):
        main_key = main_key.replace('MU UK ', '')
        if main_key=='MALS' or main_key=='TMTS':
            main_key='MALS/TMTS' 

    if main_key not in data:
        data[main_key] = {'labels': [], 'sizes': [], 'stages': [], 'opps': [], 'groups': [], 'newdeals': []}

    # Convert sizes to integer and use the maximum of size and sizeCV
    size = int(size)
    sizeCV = int(sizeCV)
    final_size = max(size, sizeCV)
    
    group = get_stage_group(stage)

    data[main_key]['labels'].append(label)
    data[main_key]['sizes'].append(final_size)
    data[main_key]['stages'].append(stage)
    data[main_key]['opps'].append(opp)
    data[main_key]['groups'].append(group)
    data[main_key]['newdeals'].append(newdeal)

# Sort the dictionary by main_key
data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
print(f"Total rows processed: {row_count}")

# Sort each main_key entry first by group order, then by label alphabetically
group_priority = {group: -i for i, group in enumerate(stage_groups.keys())}

for main_key in data:
    combined = list(zip(data[main_key]['labels'], data[main_key]['sizes'], data[main_key]['stages'], data[main_key]['opps'], data[main_key]['groups'], data[main_key]['newdeals']))
    combined.sort(key=lambda x: (group_priority.get(x[4], float('inf')), -ord(x[0][0])))  # Sort by group first, then label
    labels, sizes, stages, opps, groups, newdeals = zip(*combined)
    data[main_key]['labels'] = list(labels)
    data[main_key]['sizes'] = list(sizes)
    data[main_key]['stages'] = list(stages)
    data[main_key]['opps'] = list(opps)
    data[main_key]['groups'] = list(groups)
    data[main_key]['newdeals'] = list(newdeals)

print(data)
# Calculate the total sizes for each category
total_sizes = {key: sum(value['sizes']) for key, value in data.items()}

# Define circle widths and decreasing radii
widths = [4, 3, 3, 0.2]
radii = [sum(widths[:i+1]) for i in range(len(widths))][::-1]

# Define colors for each circle
colors = ['#e7e8ee', '#00929b', '#00bfbf', '#35b8ff']

# Create figure
fig = go.Figure()

# Add colored circles with decreasing radii
for radius, color in zip(radii, colors):
    fig.add_trace(go.Scatterpolar(
        r=[radius] * 360,
        theta=list(range(360)),
        mode='lines',
        line=dict(color="white", width=1.5),
        fill='toself',
        fillcolor=color,
        showlegend=False,  # Do not show legend for circles
        hoverinfo='skip'  # Remove theta and r in hover
    ))

label_counts = {key: len(value['labels']) for key, value in data.items()}
print(label_counts)
# Calculate the total number of labels across all categories
total_labels = sum(label_counts.values())

# Calculate angles for each segment and add segment lines
start_angle = 90
angles = {}
for category, count in label_counts.items():
    end_angle = start_angle + 360 * count / total_labels
    angles[category] = (start_angle, end_angle)
    print(f"Category {category}: start_angle={start_angle}, end_angle={end_angle}")  # Debug print
    fig.add_trace(go.Scatterpolar(
        r=[0, max(radii)],
        theta=[end_angle, end_angle],
        mode='lines',
        line=dict(color='black', width=3),
        showlegend=False,
        hoverinfo='skip'  # Remove theta and r in hover
    ))
    start_angle = end_angle

# Print angles for debugging
print("Angles Dictionary:", angles)


def split_number(n):
    # Initialize the smallest difference to be larger than 3
    min_diff = float('inf')
    result = (0, 0, 0)

    # Iterate over possible values for the first number
    for first in range(1, n // 3 + 1):
        for second in range(first + 1, (n - first) // 2 + 1):
            third = n - first - second
            if third > second:
                # Check if the difference between largest and smallest is at least 3
                if third - first >= 3:
                    diff = third - first
                    if diff < min_diff:
                        min_diff = diff
                        result = (first, second, third)
    
    return result
# def distribute_counts(count, radii):
#     # Distribute the counts across the radii values, starting from the outermost radius
#     distribution = [0] * len(radii)
#     remaining_count = count
#     for i in reversed(range(len(radii))):
#         if remaining_count <= 0:
#             break
#         # Allocate labels to the current radius
#         distribution[i] = min(remaining_count, count // len(radii) + (count % len(radii) if i == 0 else 0))
#         remaining_count -= distribution[i]
#     return distribution

def break_text_opp(text, max_length=20):
    words = text.split()  # This splits the text into words and automatically removes extra spaces
    lines = []
    current_line = ""

    for word in words:
        # Skip words that are only spaces (though the split should already handle this)
        if not word.strip():
            continue

        if len(current_line) + len(word) + 1 > max_length:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    
    if current_line:
        lines.append(current_line)
    
    return "<br>".join(lines)

def break_text_label(text, max_length=14):
    words = text.split()  # This splits the text into words and automatically removes extra spaces
    lines = []
    current_line = ""

    for word in words:
        # Skip words that are only spaces (though the split should already handle this)
        if not word.strip():
            continue

        if len(current_line) + len(word) + 1 > max_length:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    
    if current_line:
        lines.append(current_line)
    
    return "<br>".join(lines)

def calculate_angle_increment(start_angle, end_angle, count):
    if count == 0:
        return 0
    return (end_angle - start_angle) / count

# Define tolerance for boundary avoidance
tolerance = 5
counter=1

def distribute_counts(count, radii):
    # Distribute the counts across the radii values, starting from the outermost radius
    distribution = [0] * len(radii)
    remaining_count = count
    for i in reversed(range(len(radii))):
        if remaining_count <= 0:
            break
        # Allocate labels to the current radius
        distribution[i] = min(remaining_count, count // len(radii) + (count % len(radii) if i == 0 else 0))
        remaining_count -= distribution[i]
    return distribution

# def distribute_counts(total_count, radii):
#     num_radii = len(radii)
    
#     if num_radii == 1:
#         return [total_count]
    
#     elif num_radii == 2:
#         # Split labels so that more are at the larger radius
#         larger_ratio = 0.65
#         larger_count = int(total_count * larger_ratio)
#         smaller_count = total_count - larger_count
#         return [larger_count, smaller_count]

#     else:
#         # For more than two radii, distribute proportionally with a slight preference for larger radii
#         base_count = total_count // num_radii
#         extra = total_count % num_radii
#         distribution = [base_count + (1 if i < extra else 0) for i in range(num_radii)]
#         # Ensure more labels are at larger radii
#         for i in range(num_radii - 1):
#             if distribution[i] < distribution[i + 1]:
#                 distribution[i] += 1
#                 distribution[i + 1] -= 1
#         return distribution

for category, details in data.items():
    start_angle, end_angle = angles.get(category, (0, 360))  # Default to full circle if category not found
    group_counts = {group: 0 for group in stage_groups}
    group_counts['Others'] = 0  # Ensure 'Others' is included

    for group in details['groups']:
        group_counts[group] += 1

    # Track plotted labels and opps per group to avoid duplication
    plotted_labels = {group: set() for group in stage_groups}

    for group in stage_groups:
        if group_counts[group] > 0:
            if group == 'group_1':
                radius_values = [3.3, 2.4, 1.3]
            elif group == 'group_2':
                radius_values = [6.1, 4.9]
            else:
                radius_values = [7.9,9.1]

            distribution = distribute_counts(group_counts[group], radius_values)
            
            # Sort total_labels by label in reverse alphabetical order
            total_labels = sorted(
                [(label, size, stage, group_label, opp, newdeals) 
                for label, size, stage, group_label, opp, newdeals in zip(details['labels'], details['sizes'], details['stages'], details['groups'], details['opps'], details['newdeals']) if group_label == group],
                key=lambda x: x[0], reverse=True  # Sort by label, reverse alphabetical order
            )

            # Calculate the angle increment for each radius based on the count of labels
            angle_increments = [
                calculate_angle_increment(start_angle, end_angle, count)
                for count in distribution
            ]

            # Initialize angles for each radius
            current_angles = [start_angle + (angle_increment / 2) for angle_increment in angle_increments]

            # Loop through radii first, then through angles
            while total_labels:
                for radius_index, radius in enumerate(radius_values):
                    if not total_labels:
                        break

                    if distribution[radius_index] > 0:
                        # Get the next label
                        label, size, stage, group_label, opp, newdeals = total_labels.pop(0)

                        # Ensure this label and opp combination is not already plotted
                        if (label, opp) in plotted_labels[group]:
                            continue

                        # Adjust angle slightly to avoid plotting directly on start/end lines
                        adjusted_angle = current_angles[radius_index]

                        text_color = 'white' if group == 'group_3' else 'black'
                        if group=='group_2' and category in ['HMRC','ET&U','CPRD']:
                            label_fontsize = 8 if group in ['group_1', 'group_2'] else 8
                            detail_fontsize = 7 if group in ['group_1'] else 7
                        else:
                            label_fontsize = 9 if group in ['group_1', 'group_2'] else 9
                            detail_fontsize = 7 if group in ['group_1'] else 8

                        # Prepare text and hover text with counter included
                        if size > 0:
                            label_text = f"<b style='font-size:{label_fontsize}px; font-family:Arial, sans-serif'>{break_text_label(label.strip())}</b><br><b style='font-size:{detail_fontsize}px; font-family:Arial, sans-serif'>{break_text_opp(get_first_two_words(opp))}<br>(£{round(size)}M)</b>"
                            hover_text = f"<b style='font-size:{label_fontsize}px; font-family:Arial, sans-serif'>{label.strip()}</b><br><span style='font-size:{detail_fontsize}px; font-family:Arial, sans-serif'>({opp})<br>(£{round(size)}M)</span>"
                        else:
                            label_text = f"<b style='font-size:{label_fontsize}px; font-family:Arial, sans-serif'>{break_text_label(label.strip())}</b><br><b style='font-size:{detail_fontsize}px; font-family:Arial, sans-serif'>{break_text_opp(get_first_two_words(opp))}</b>"
                            hover_text = f"<b style='font-size:{label_fontsize}px; font-family:Arial, sans-serif'>{label.strip()}</b><br><span style='font-size:{detail_fontsize}px; font-family:Arial, sans-serif'>({opp})</span>"

                        # Add text label
                        fig.add_trace(go.Scatterpolar(
                            r=[radius],
                            theta=[adjusted_angle],
                            mode='text',
                            text=[label_text],
                            showlegend=False,
                            textfont=dict(size=detail_fontsize, color=text_color),
                            hoverinfo='text',
                            hovertext=hover_text
                        ))
                        
                        # Adjusted angles from 90 to 450 degrees
                        if group=='group_1':
                            offset_angle = 5 if adjusted_angle < 90 or adjusted_angle > 270 else -7
                            offset_radius = 0.5 if adjusted_angle < 180 or adjusted_angle > 360 else -0.5
                        elif group=='group_2':
                            offset_angle = 4 if adjusted_angle < 90 or adjusted_angle > 270 else -4
                            offset_radius = 0.4 if adjusted_angle < 180 or adjusted_angle > 360 else -0.4
                        else:
                            offset_angle = 3 if adjusted_angle < 90 or adjusted_angle > 270 else -3
                            offset_radius = 0.4 if adjusted_angle < 180 or adjusted_angle > 360 else -0.4
                        figure_size = 10

                        # Add markers for new deals
                        if newdeals == 'NEW':
                            fig.add_trace(go.Scatterpolar(
                                r=[radius + offset_radius],
                                theta=[adjusted_angle + offset_angle],
                                mode='markers',
                                marker=dict(size=figure_size, symbol='triangle-up', color='white', line=dict(width=0.3)),
                                showlegend=False,
                                hoverinfo='skip'
                            ))

                        elif newdeals == 'Sold':
                            fig.add_trace(go.Scatterpolar(
                                r=[radius + offset_radius],
                                theta=[adjusted_angle + offset_angle],
                                mode='markers',
                                marker=dict(size=figure_size, symbol='square', color='#90EE90', line=dict(width=0.1)),
                                showlegend=False,
                                hoverinfo='skip'
                            ))

                        elif newdeals == 'Lost' or newdeals=='Dropped':
                            fig.add_trace(go.Scatterpolar(
                                r=[radius + offset_radius],
                                theta=[adjusted_angle + offset_angle],
                                mode='markers',
                                marker=dict(size=figure_size, symbol='square', color='red', line=dict(width=0.1)),
                                showlegend=False,
                                hoverinfo='skip'
                            ))

                        # Mark this label as plotted and increment the counter
                        plotted_labels[group].add((label, opp))
                        counter += 1  # Increment the counter after each label is plotted

                        # Increment the angle for the current radius
                        current_angles[radius_index] += angle_increments[radius_index]

# Add segment labels
for category, (start_angle, end_angle) in angles.items():
    angle = (start_angle + end_angle) / 2
    size_value = total_sizes[category]
    if angle>250 and angle<290 or angle>420 and angle<450:
            radius=[max(radii) + 1.8]
    else: radius=[max(radii)+1.8]
    fig.add_trace(go.Scatterpolar(
        r=radius,
        theta=[angle],
        mode='text',
        text=[f"{category}"],
        showlegend=False,
        textfont=dict(size=15, weight='bold', color='white'),  # Smaller font size for segment labels
        hoverinfo='skip'  # Remove theta and r in hover
    ))

font_colors = {'Proactive': 'triangle-up'}
for stage, symbols in font_colors.items():
    fig.add_trace(go.Scatterpolar(
        r=[None],
        theta=[None],
        mode='markers',
        marker=dict(size=10, symbol=symbols, color='white', line=dict(width=1)),
        showlegend=False,
        name=f"Stage : {stage}",
        hoverinfo='skip'
    ))

# Add threshold labels with white background and black bold text
threshold_labels = [
    {'r': 4, 'theta': 90, 'text': 'SS 1-3'},
    {'r': 7, 'theta': 90, 'text': 'SS 4+'},
    {'r':0, 'theta' : 90, 'text': 'SS 0+'}
]

for label in threshold_labels:

    # Add a white rectangle behind the text
    fig.add_trace(go.Scatterpolar(
        r=[label['r']],
        theta=[label['theta']],
        mode='markers',
        marker=dict(size=40, symbol='circle', color='white', opacity=1),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[label['r']],
        theta=[label['theta']],
        mode='text',
        text=[label['text']],
        showlegend=False,
        name='Stage Threshold',
        textfont=dict(size=12, color="black", weight='bold'),  # Make the text black and bold
        textposition='middle center',
        hoverinfo='skip',
        texttemplate='%{text}',  # Ensures text is displayed
    ))

fig.update_layout(
    width=1080,
    height=1080,
    polar=dict(
        radialaxis=dict(visible=False),
        angularaxis=dict(visible=False),
        bgcolor='rgba(0,0,0,0)',  # Set polar background to transparent
    ),
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',  # Set background to transparent
    plot_bgcolor='rgba(0,0,0,0)'
)

import plotly.io as pio
pio.write_image(fig, 'imagelabel.png',format='png',scale=4, width=1080, height=1080)
# Show figure
config = {
  'toImageButtonOptions': {
    'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'custom_image',
    'height': 1080,
    'width': 1080,
    'scale':4 # Multiply title/legend/axis/canvas sizes by this factor
  }
}
fig.show(config=config)
