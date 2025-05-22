from datetime import datetime
from typing import List, Dict, Any

class Member:
    def __init__(self, member_id: str, name: str, age: int, membership_type: str, fitness_goals: str):
        self.member_id = member_id
        self.name = name
        self.age = age
        self.membership_type = membership_type
        self.fitness_goals = fitness_goals
        self.class_bookings = []
        self.progress_data = []
        
    def update_membership(self, new_type: str) -> None:
        self.membership_type = new_type
        
    def book_class(self, class_obj) -> bool:
        if class_obj not in self.class_bookings:
            self.class_bookings.append(class_obj)
            return True
        return False
    
    def track_progress(self, progress_data: Dict[str, Any]) -> None:
        progress_data['date'] = datetime.now()
        self.progress_data.append(progress_data)
        
    def get_progress(self) -> List[Dict[str, Any]]:
        return self.progress_data
    
    def cancel_class(self, class_obj) -> bool:
        if class_obj in self.class_bookings:
            self.class_bookings.remove(class_obj)
            return True
        return False


class Trainer:
    def __init__(self, trainer_id: str, name: str, specialization: str):
        self.trainer_id = trainer_id
        self.name = name
        self.specialization = specialization
        self.assigned_classes = []
        
    def assign_class(self, class_obj) -> bool:
        if class_obj not in self.assigned_classes:
            self.assigned_classes.append(class_obj)
            return True
        return False
        
    def view_schedule(self) -> List:
        return self.assigned_classes


class FitnessClass:
    def __init__(self, class_id: str, name: str, capacity: int, schedule: str):
        self.class_id = class_id
        self.name = name
        self.trainer = None
        self.capacity = capacity
        self.current_enrollments = 0
        self.schedule = schedule
        self.enrolled_members = []
    
    def enroll_member(self, member) -> bool:
        if self.current_enrollments < self.capacity and member not in self.enrolled_members:
            self.enrolled_members.append(member)
            self.current_enrollments += 1
            return True
        return False
    
    def cancel_booking(self, member) -> bool:
        if member in self.enrolled_members:
            self.enrolled_members.remove(member)
            self.current_enrollments -= 1
            return True
        return False
    
    def assign_trainer(self, trainer) -> bool:
        self.trainer = trainer
        return True


class Transaction:
    def __init__(self, transaction_id: str, member, amount_paid: float, service: str):
        self.transaction_id = transaction_id
        self.member = member
        self.amount_paid = amount_paid
        self.payment_date = datetime.now()
        self.service = service
        
    def process_payment(self, member, amount: float, service: str) -> bool:
        self.member = member
        self.amount_paid = amount
        self.service = service
        self.payment_date = datetime.now()
        return True
    
    def generate_receipt(self) -> str:
        receipt = f"""
        Receipt for Transaction #{self.transaction_id}
        Member: {self.member.name}
        Membership: {self.service}
        Date: {self.payment_date.strftime('%Y-%m-%d')}
        Amount Paid: ${self.amount_paid:.2f}
        """
        return receipt


class FitnessManagementSystem:
    def __init__(self):
        self.members = []
        self.trainers = []
        self.fitness_classes = []
        self.transactions = []
        
    def register_member(self, member: Member) -> bool:
        if member not in self.members:
            self.members.append(member)
            return True
        return False
    
    def view_members(self) -> List[Member]:
        return self.members
    
    def add_trainer(self, trainer: Trainer) -> bool:
        if trainer not in self.trainers:
            self.trainers.append(trainer)
            return True
        return False
    
    def schedule_class(self, class_obj: FitnessClass) -> bool:
        if class_obj not in self.fitness_classes:
            self.fitness_classes.append(class_obj)
            return True
        return False
    
    def generate_revenue_report(self) -> Dict[str, Any]:
        total_revenue = sum(t.amount_paid for t in self.transactions)
        active_members = len(self.members)
        
        class_popularity = {}
        for cls in self.fitness_classes:
            class_popularity[cls.name] = cls.current_enrollments
            
        top_class = max(class_popularity.items(), key=lambda x: x[1]) if class_popularity else None
        
        return {
            "total_revenue": total_revenue,
            "top_class": top_class,
            "active_members": active_members
        }
    
    def view_member_progress(self, member_id: str) -> List[Dict[str, Any]]:
        for member in self.members:
            if member.member_id == member_id:
                return member.get_progress()
        return []
    
    def cancel_membership(self, member_id: str) -> bool:
        for member in self.members:
            if member.member_id == member_id:
                self.members.remove(member)
                return True
        return False
    
    def add_transaction(self, transaction: Transaction) -> bool:
        self.transactions.append(transaction)
        return True
    
    def find_member_by_id(self, member_id: str) -> Member:
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
