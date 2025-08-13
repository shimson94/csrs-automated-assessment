export interface Activity {
    id: number;
    time: string;
    title: string;
    description: string;
    type: 'submission' | 'grading' | 'assignment';
  }
  
  const ActivityCard = ({ activity }: { activity: Activity }) => {
    const borderColors = {
      submission: 'border-blue-500',
      grading: 'border-green-500',
      assignment: 'border-yellow-500'
    };
  
    return (
      <div className={`border-l-4 ${borderColors[activity.type]} pl-4 p-3 bg-white rounded-r-lg hover:shadow-md transition-shadow`}>
        <p className="text-sm text-black">{activity.time}</p>
        <p className="font-medium">{activity.title}</p>
        <p className="text-sm text-gray-500">{activity.description}</p>
      </div>
    );
  };
  
  export default ActivityCard;