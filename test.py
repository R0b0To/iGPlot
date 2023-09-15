color_mapping = {
    'O Bearman': '#FF8700',
    'P Riccardi': '#FF8700',
    'S Vettel': '#D3D3D3',
    'E Moss': '#D3D3D3',
    'E Tanolo': '#0000CD'
}

sorted_names = ['N Wong', 'M Kevinsen', 'C Stoner', 'J Moss', 'S Vettel', 'D Mansell', 'E Tanolo', 'D Verstappen', 'P Riccardi', 'I Lutrova', 'V Aznabaev', 'L Stroll', 'R Rizzoli', 'L Almeida', 'W Wieczorek', 'V Martins', 'С Кристиночки', 'E Moss', 'J Opmeer', 'M Croes', 'J Fangio', 'N Panis', 'T Lindroos', 'O Bearman']

label_colors = [color_mapping.get(name, 'white') for name in sorted_names]
print(label_colors)
