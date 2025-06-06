<?php

namespace App\Livewire;

use Livewire\Component;

class ChatAssistant extends Component
{
    public $conversations = [];
    public $activeConversation;
    public $messages = [];
    public $newMessage = '';

    public function mount()
    {
        $this->conversations = [
            ['id' => 1, 'title' => 'Conversazione 1'],
            ['id' => 2, 'title' => 'Conversazione 2'],
        ];
        //fare chiamata api che me le pesca da db laravel

        $this->activeConversation = 1;
        //metto come prima conversazione quella con id ultimo

        $this->messages = [
            ['sender' => 'assistant', 'message' => 'Ciao! Come posso aiutarti?']
        ];
    }

    public function selectConversation($id)
    {
        $this->activeConversation = $id;
        $this->messages = [
            ['sender' => 'assistant', 'message' => "Hai selezionato la conversazione #$id."]
        ];
        // quando chiamo l'altra devo caricare da db
    }

    public function sendMessage()
    {
        if (trim($this->newMessage) === '') return;

        $this->messages[] = ['sender' => 'user', 'message' => $this->newMessage];
        $this->messages[] = ['sender' => 'assistant', 'message' => 'Sto pensando... 😉'];
        $this->newMessage = '';
        // SALVO IL MESSAGGIO SUL DB TODO chiamare api python che salva a db
        // meccanismo di polling, che ogni 5 secondi verifica se ci sono nuovi messaggi
        //api che ti ritorna tutti i messaggi
        //api che ritorna tutte le conversazioni
        //api dentro laravel /conversations che ritorna tutte le conversazioni
        //api dentro laravel /conversations/{id} che ritorna tutti i messaggi della conversazione
        // sender va collegato a un id utente
        
    }

    public function render()
    {
        return view('livewire.chat-assistant');
    }
}
