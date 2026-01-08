# Updated code for the choropleth map cell
# This includes all US states, even those without data

# Create complete list of all US state abbreviations
all_us_states = pd.DataFrame({
    'state': [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
    ]
})

# Merge with actual revenue data, filling missing states with 0
state_revenue_complete = all_us_states.merge(state_revenue, on='state', how='left')
state_revenue_complete['revenue'] = state_revenue_complete['revenue'].fillna(0)

# Create choropleth map
fig = px.choropleth(
    state_revenue_complete,
    locations='state',
    color='revenue',
    locationmode='USA-states',
    scope='usa',
    title=f'Revenue by State - {CURRENT_START_YEAR}',
    color_continuous_scale='Blues',
    labels={'revenue': 'Revenue (USD)'}
)

fig.update_layout(
    title_font_size=16,
    title_font_family='Arial',
    geo=dict(bgcolor='rgba(0,0,0,0)')
)

fig.show()
