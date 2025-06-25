<div class="h-[85vh] rounded-xl overflow-hidden border shadow-md flex" style="height: 75vh; border: 2px solid #000;">

    <!-- ░░░ SIDEBAR ░░░ -->
    <div class="sidebar flex flex-col overflow-y-auto" style="width:17rem;">

        <!-- Header -->
        <div class="sidebar-header p-4 flex items-center justify-between">
            <h2 class="text-lg font-bold text-white">Conversazioni</h2>

            <!-- + -->
            <button
                wire:click="openModal"
                class="plus-button w-8 h-8 grid place-content-center rounded-lg bg-black text-white border border-white/40 hover:scale-105 transition">
                +
            </button>
        </div>

        <!-- Modal nuova conversazione -->
        @if ($showModal)
            <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                <div class="modal p-6 rounded-xl w-full max-w-md shadow-xl space-y-4" style="border: 2px solid black;">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white" style="color: black;">Nuova Conversazione</h3>

                    <div>
                        <label class="block text-sm text-gray-700 dark:text-gray-300 mb-1" style="color: black; margin-bottom: 0.2em;">Titolo</label>
                        <input  type="text"
                                wire:model.defer="newConversationTitle"
                                class="modal-input w-full px-4 py-2 rounded-lg border dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500" 
                                style="background-color: white; color:black;"/>
                    </div>

                    <div class="flex justify-end gap-2 pt-2">
                        <button wire:click="closeModal" type="button"
                                class="button-annulla px-4 py-2 bg-gray-300 dark:bg-gray-600 rounded-lg text-black dark:text-white hover:bg-gray-400 dark:hover:bg-gray-700">
                            Annulla
                        </button>
                        <button wire:click="createConversation" type="button"
                                class="button-crea px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg border-2 border-blue-700">
                            Crea
                        </button>
                    </div>
                </div>
            </div>
        @endif

        <!-- Elenco conversazioni -->
        <div class="p-4 space-y-3">
            @foreach ($conversations as $conv)
                <button
                    wire:click="selectConversation({{ $conv['id'] }})"
                    class="conversation-btn {{ $activeConversation === $conv['id'] ? 'active-conversation' : '' }}">
                    {{ $conv['title'] }}
                </button>
            @endforeach
        </div>
    </div>

    <!-- ░░░ AREA CHAT ░░░ -->
    <div class="flex flex-col flex-1">

        <!-- Messaggi -->
        <div wire:poll.1s="refreshMessages" class="chat-wrapper flex-1 overflow-y-auto p-6 space-y-4">

            @if ($hasMore)
                <div class="text-center">
                    <button wire:click="loadMore"
                        class="mt-4 px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600">
                        Carica altri
                    </button>
                </div>
            @endif

            @foreach ($loaded as $message)
                <div class="w-full flex {{ $message['sender'] === 'user' ? 'justify-end' : 'justify-start' }}">
                    <div class="bubble-common {{ $message['sender'] === 'user' ? 'bubble-user' : 'bubble-assistant' }}">
                        @if($message['sender'] === 'assistant' && $message['content'] === 'Sto pensando…')
                            <div class="flex items-center gap-2">
                                Sto pensando <x-filament::loading-indicator class="h-5 w-5" />
                            </div>
                        @else
                            {{ $message['content'] }}
                        @endif
                    </div>
                </div>
            @endforeach
        </div>

        <!-- Input -->
        <form wire:submit.prevent="sendMessage" class="chat-input-bar flex items-center gap-3 p-4 border-t border-black/20">
            <input  type="text"
                    wire:model.defer="newMessage"
                    placeholder="Scrivi un messaggio..."
                    class="flex-1 rounded-full px-4 py-2 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500" 
                    style="color: black;"/>

            <button type="submit" class="send-btn">
                Invia
            </button>
        </form>
    </div>
</div>
