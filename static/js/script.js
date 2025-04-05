document.addEventListener("DOMContentLoaded", function () {
    const sampleBtn = document.getElementById("fill-sample");

    if (sampleBtn) {
        sampleBtn.addEventListener("click", function () {
            const sampleData = {
                pregnancies: 2,
                glucose: 130,
                blood_pressure: 70,
                skin_thickness: 28,
                insulin: 100,
                bmi: 30.5,
                diabetes_pedigree: 0.4,
                age: 35
            };

            Object.entries(sampleData).forEach(([key, value]) => {
                const input = document.querySelector(`[name="${key}"]`);
                if (input) input.value = value;
            });
        });
    }
});