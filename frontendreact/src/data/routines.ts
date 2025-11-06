import { Routine } from '../types';

export const routines: Routine[] = [
  {
    id: 'surya-namaskar',
    name: 'Surya Namaskar',
    description: 'A sequence of 12 yoga poses to greet the sun.',
    difficulty: 'intermediate',
    asanas: [
      { id: 1, name: 'Pranamasana', sanskritName: 'Prayer Pose', image: 'https://images.pexels.com/photos/3822356/pexels-photo-3822356.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 2, name: 'Hastauttanasana', sanskritName: 'Raised Arms Pose', image: 'https://images.pexels.com/photos/3822455/pexels-photo-3822455.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 3, name: 'Hastapadasana', sanskritName: 'Hand to Foot Pose', image: 'https://images.pexels.com/photos/3822164/pexels-photo-3822164.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 4, name: 'Ashwa Sanchalanasana', sanskritName: 'Equestrian Pose', image: 'https://images.pexels.com/photos/3822622/pexels-photo-3822622.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 5, name: 'Dandasana', sanskritName: 'Stick Pose', image: 'https://images.pexels.com/photos/4056535/pexels-photo-4056535.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 6, name: 'Ashtanga Namaskara', sanskritName: 'Eight-Limbed Salutation', image: '/images/ashtanga-namaskara.jpg' },
      { id: 7, name: 'Bhujangasana', sanskritName: 'Cobra Pose', image: 'https://images.pexels.com/photos/3822906/pexels-photo-3822906.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 8, name: 'Adho Mukha Svanasana', sanskritName: 'Downward-Facing Dog Pose', image: 'https://images.pexels.com/photos/3822356/pexels-photo-3822356.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 9, name: 'Ashwa Sanchalanasana', sanskritName: 'Equestrian Pose', image: 'https://images.pexels.com/photos/3822622/pexels-photo-3822622.jpeg?auto=compress&cs=tinysrgb&w=800' },
      { id: 10, name: 'Hastapadasana', sanskritName: 'Hand to Foot Pose', image: '/images/hastapadasana.jpg' },
      { id: 11, name: 'Hastauttanasana', sanskritName: 'Raised Arms Pose', image: '/images/hastauttanasana.jpg' },
      { id: 12, name: 'Tadasana', sanskritName: 'Mountain Pose', image: '/images/tadasana.jpg' },

    ],
  },
];