<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB; 

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('documents', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('site_id');
            $table->text('title');
            $table->text('url');
            $table->text('hash');
            $table->text('content');
            $table->foreign('site_id')->references('id')->on('sites')->onDelete('cascade');
        });

        DB::statement('ALTER TABLE documents ADD COLUMN document_embedding vector(1024);');
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('documents');
    }
};
