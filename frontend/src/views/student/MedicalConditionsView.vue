<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md mb-4">
            <div class="bg-orange-50 border-l-4 border-orange-400 rounded-lg p-4 mb-4">
                <div class="font-semibold mb-2">Active Conditions</div>
                <div class="mb-2">
                    <span class="inline-block bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs mr-2 mb-1">Type 1
                        Diabetes</span>
                    <span class="inline-block bg-yellow-100 text-yellow-700 px-2 py-1 rounded-full text-xs mb-1">Food
                        Allergy (Nuts)</span>
                </div>
                <div class="text-xs text-gray-700">Monitor blood sugar levels and avoid nuts/tree nuts</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
                <div class="font-semibold mb-2">Dietary Restrictions</div>
                <div class="text-xs text-gray-700">
                    • Low sugar diet (diabetic-friendly)<br>
                    • Nut-free foods only<br>
                    • Limit processed foods<br>
                    • No artificial sweeteners
                </div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
                <div class="font-semibold mb-2">Current Medications</div>
                <div class="text-xs text-gray-700 mb-2">
                    <div class="mb-1"><strong>Insulin (Rapid-acting)</strong><br><span>Before meals • Next: 6:00
                            PM</span></div>
                    <div><strong>Multivitamin</strong><br><span>Once daily • Next: Tomorrow 8:00 AM</span></div>
                </div>
            </div>
            <div class="flex flex-col gap-2">
                <button class="btn-secondary">Add New Condition</button>
                <button class="btn-secondary">Add Medication</button>
                <button class="btn-primary">Upload Medical Report</button>
            </div>
        </div>
        <div class="text-xs text-gray-400 mt-4">Medical Conditions</div>
    </div>
</template>

<script setup>
// Placeholder logic for add condition, medication, upload
</script>