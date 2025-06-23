<?php

namespace App\Filament\Resources;

use App\Filament\Resources\StatisticResource\Pages;
use App\Filament\Resources\StatisticResource\RelationManagers;
use App\Models\Statistic;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

class StatisticResource extends Resource
{
    protected static ?string $model = Statistic::class;

    protected static ?string $navigationIcon = 'heroicon-o-chart-bar';

    protected static ?string $navigationGroup = 'Data Management';
    
    protected static ?int $navigationSort = 5;

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\TextInput::make('document_id')
                    ->required()
                    ->numeric(),
                Forms\Components\Textarea::make('model_llm')
                    ->required()
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('model_embedding')
                    ->required()
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('token_prompt')
                    ->numeric(),
                Forms\Components\TextInput::make('token_response')
                    ->numeric(),
                Forms\Components\TextInput::make('token_used')
                    ->numeric(),
                Forms\Components\Textarea::make('prompt')
                    ->required()
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('model_max_tokens')
                    ->required()
                    ->numeric(),
                Forms\Components\TextInput::make('model_temperature')
                    ->required()
                    ->numeric(),
                Forms\Components\Textarea::make('model_llm_api')
                    ->required()
                    ->columnSpanFull(),
                Forms\Components\Textarea::make('model_embedding_api')
                    ->required()
                    ->columnSpanFull(),
                Forms\Components\TextInput::make('chunk_size')
                    ->required()
                    ->numeric(),
                Forms\Components\TextInput::make('chunk_overlap')
                    ->required()
                    ->numeric(),
                Forms\Components\TextInput::make('number_response_llm')
                    ->numeric(),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('id')->searchable(),
                Tables\Columns\TextColumn::make('document_id')->searchable(),
                Tables\Columns\TextColumn::make('model_llm')->searchable(),
                Tables\Columns\TextColumn::make('model_embedding')->searchable(),
                Tables\Columns\TextColumn::make('token_prompt')->searchable(),
                Tables\Columns\TextColumn::make('token_response')->searchable(),
                Tables\Columns\TextColumn::make('token_used')->searchable(),
                Tables\Columns\TextColumn::make('chunk_size')->searchable(),
                Tables\Columns\TextColumn::make('chunk_overlap')->searchable(),
                Tables\Columns\TextColumn::make('number_response_llm')->searchable(),
                Tables\Columns\TextColumn::make('prompt')->searchable(),
                Tables\Columns\TextColumn::make('model_max_tokens')->searchable(),
                Tables\Columns\TextColumn::make('model_temperature')->searchable(),
                Tables\Columns\TextColumn::make('model_llm_api')->searchable(),
                Tables\Columns\TextColumn::make('model_embedding_api')->searchable(),
                Tables\Columns\TextColumn::make('created_at')->searchable(),
            ])
            ->filters([
                //
            ])
            ->actions([
                // Tables\Actions\EditAction::make(),
                Tables\Actions\DeleteAction::make(),

            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListStatistics::route('/'),
            'create' => Pages\CreateStatistic::route('/create'),
            'edit' => Pages\EditStatistic::route('/{record}/edit'),
        ];
    }
}
