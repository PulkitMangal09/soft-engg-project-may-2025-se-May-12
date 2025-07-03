<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md flex flex-col h-[600px]">
            <div class="bg-gray-50 rounded-lg p-3 text-xs text-center text-gray-600 mb-2">
                AI Assistant trained on your health conditions and dietary needs
            </div>
            <div class="flex-1 overflow-y-auto mb-2">
                <div class="mb-2 flex justify-start">
                    <div class="bg-gray-200 text-gray-800 rounded-lg p-2 max-w-[70%]">Hi! I'm your personal diet
                        assistant. I know about your diabetes and nut allergy. How can I help you today? 🥗</div>
                </div>
                <div class="mb-2 flex justify-end">
                    <div class="bg-emerald-500 text-white rounded-lg p-2 max-w-[70%]">Can I eat pizza for dinner? I'm
                        craving it</div>
                </div>
                <div class="mb-2 flex justify-start">
                    <div class="bg-gray-200 text-gray-800 rounded-lg p-2 max-w-[70%]">
                        Pizza can be part of your diet with some modifications! Here's what I recommend:<br>
                        ✅ Choose thin crust to reduce carbs<br>
                        ✅ Load up on vegetables as toppings<br>
                        ✅ Ask for light cheese<br>
                        ❌ Avoid processed meats (high sodium)<br>
                        Since you have diabetes, pair it with a salad and monitor your blood sugar 2 hours after eating.
                        Would you like some healthier pizza recipes?
                    </div>
                </div>
                <div class="mb-2 flex justify-end">
                    <div class="bg-emerald-500 text-white rounded-lg p-2 max-w-[70%]">Yes! And can you check if the
                        restaurant uses nuts in their pizza?</div>
                </div>
                <div class="mb-2 flex justify-start">
                    <div class="bg-gray-200 text-gray-800 rounded-lg p-2 max-w-[70%]">
                        Great question! Always ask about:<br>
                        • Pesto sauces (often contain pine nuts)<br>
                        • Specialty cheeses with nuts<br>
                        • Cross-contamination in kitchen<br>
                        <br>
                        Here's a diabetes-friendly pizza recipe:<br>
                        🍕 Cauliflower crust with vegetables<br>
                        🧀 Part-skim mozzarella<br>
                        🍅 Fresh tomato sauce (low sodium)<br>
                        🥬 Spinach, bell peppers, mushrooms<br>
                        <br>
                        This keeps carbs under 30g per slice!
                    </div>
                </div>
            </div>
            <div class="flex gap-2 mt-2">
                <input type="text" class="form-input flex-1" placeholder="Ask about foods, recipes, or nutrition...">
                <button class="btn-primary px-4">➤</button>
            </div>
        </div>
        <div class="text-xs text-gray-400 mt-4">Diet Chat Bot</div>
    </div>
</template>

<script setup>
// Placeholder logic for chat
</script>