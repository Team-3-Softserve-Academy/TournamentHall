document.addEventListener('DOMContentLoaded', () => {
    const roleRadios = document.querySelectorAll(
        'input[name="role"]'
    );

    const attributes = document.getElementById('attributes-section');
    const profile = document.getElementById('profile-section');

    function updateRoleSections() {
        const selectedRole = document.querySelector(
            'input[name="role"]:checked'
        );

        if (!selectedRole) return;

        if (selectedRole.value === 'Knight') {
            attributes.style.display = 'block';
            profile.style.display = 'block';
        } else if (selectedRole.value === 'Lord') {
            attributes.style.display = 'none';
            profile.style.display = 'block';
        } else {
            attributes.style.display = 'none';
            profile.style.display = 'none';
        }
    }

    roleRadios.forEach(radio => {
        radio.addEventListener('change', updateRoleSections);
    });

    updateRoleSections();
});
