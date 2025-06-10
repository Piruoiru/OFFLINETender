<div class="h-[85vh] bg-white dark:bg-gray-900 rounded-xl overflow-hidden border shadow-md">
    <div class="flex h-full w-full" style="height: 75vh;">
        <!-- Sidebar Conversazioni -->
        <div class="bg-gray-100 dark:bg-gray-800 p-4 border-r dark:border-gray-700 flex flex-col overflow-y-auto" style="width: 17rem;">
            <h2 class="text-lg font-bold mb-4 text-gray-800 dark:text-white">Conversazioni</h2>
        
            <div class="space-y-2">
                @foreach ($conversations as $conv)
                    <button wire:click="selectConversation({{ $conv['id'] }})"
                            class="block w-full text-left px-4 py-2 rounded-lg font-medium transition
                                {{ $activeConversation === $conv['id']
                                    ? 'bg-blue-600 text-black dark:bg-blue-500 dark:text-white'
                                    : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-blue-100 dark:hover:bg-gray-600' }}">
                        {{ $conv['title'] }}
                    </button>
                @endforeach
            </div>
        </div>
        <div class="flex flex-col w-full h-full">
            <!-- Area Chat -->
            <div class="flex flex-col flex-1 bg-gray-50 dark:bg-gray-900 overflow-y-auto">
                <!-- Messaggi -->
                <div wire:poll.5s="refreshMessages" class="flex-1 overflow-y-auto p-6 space-y-4">
                    @foreach ($messages as $message)
                        <div class="w-full flex {{ $message['sender'] === 'user' ? 'justify-end' : 'justify-start' }}">
                            <div class="max-w-lg px-4 py-2 rounded-xl shadow
                                {{ $message['sender'] === 'user'
                                    ? 'bg-blue-500 text-black'
                                    : 'bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-white' }}">
                                {{ $message['message'] }}
                            </div>
                        </div>
                    @endforeach
                </div>
    
                <!-- Input -->
                <form wire:submit.prevent="sendMessage" class="flex items-center gap-3 p-4 border-t dark:border-gray-700 bg-white dark:bg-gray-800">
                    <input type="text" wire:model.defer="newMessage"
                        class="flex-1 border dark:border-gray-600 rounded-full px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Scrivi un messaggio..." />
    
                    <button type="submit"
                            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full font-semibold transition">
                        Invia
                    </button>
                </form>
            </div>
        </div>
    </div> 
</div>
