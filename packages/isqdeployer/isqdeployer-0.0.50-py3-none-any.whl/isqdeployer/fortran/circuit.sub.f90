






! module mod_Circuit 
!   implicit none 


!   type,public::Circuit
!       private
!       logical::initialized = .False.
!       integer*8::Nq 
!       integer*8::d 
!       complex*16,allocatable::S(:)

!       contains
!           procedure,pass::Initialization 
!           procedure,pass::getState
!           procedure,pass::OneQubitGate => U2 
!           procedure,pass::TwoQubitGate => U4 
!           procedure,pass::runWithGatesFile
!           procedure,pass::stdoutMeasurement
!   endtype

!   private::Initialization
!   private::getState
!   private::U2,U4 
!   private::runWithGatesFile
!   private::stdoutMeasurement

!   contains

!   subroutine Initialization(self,Nq)
!       implicit none 
!       class(Circuit),intent(inout)::self
!       integer*8,intent(in)::Nq 
!       ! --------------------------
!       if (self%initialized) deallocate(self%S) 
!       self%initialized = .True. 
!       self%Nq = Nq 
!       allocate(self%S(0:2_8**self%Nq-1_8))
!       self%S = (0._8,0._8) 
!       self%S(0) = (1._8,0._8)
!       self%d = 2_8**self%Nq 
!   endsubroutine


!   function getState(self) result(state)
!       implicit none 
!       class(Circuit),intent(inout)::self
!       complex*16::state(self%d) 
!       ! ---------------------------
!       state = self%s
!   endfunction

!   subroutine U2(self,i,U)
!       implicit none
!       class(Circuit),intent(inout)::self
!       integer*8,intent(in)::i 
!       complex*16,intent(in)::U(2,2) 
!       ! ----------------------
!       complex*16::tmpS(0:self%d-1),a,b 
!       integer*8::w ,w0,w1 
!       tmpS = (0._8,0._8) 
!       Do w = 0, self%d-1_8 
!           ! write(*,*)w,i,999965
!           w0 = ibclr( w , i )
!           w1 = ibset( w , i ) 
!           if (btest( w,i )) then
!               a = U(1,2) 
!               b = U(2,2)
!           else 
!               a = U(1,1) 
!               b = U(2,1)
!           endif 
!           tmpS(w0) = tmpS(w0) + a * self%s(w) 
!           tmpS(w1) = tmpS(w1) + b * self%s(w)  
!       enddo
!       self%s = tmps 
!   endsubroutine

!   subroutine U4(self,i,j,U)
!       implicit none
!       class(Circuit),intent(inout)::self
!       integer*8,intent(in)::i,j 
!       complex*16,intent(in)::U(4,4) 
!       ! ----------------------
!       complex*16::tmpS(0:self%d-1) 
!       integer*8::II,IA,IB,w 
!       tmpS = (0._8,0._8) 
!       Do w = 0, self%d-1_8
!           if (btest(w,i)) then 
!               IA = 1_8 
!           else 
!               IA = 0_8 
!           endif
!           if (btest(w,j)) then 
!               IB = 1_8
!           else
!               IB = 0_8 
!           endif  
!           II = IA * 2 + IB + 1_8 
!           IA = ibclr(ibclr(w,i),j); tmpS(IA) = tmpS(IA) + U(1,II) * self%s(w) 
!           IA = ibset(ibclr(w,i),j); tmps(IA) = tmps(IA) + U(2,II) * self%s(w) 
!           IA = ibclr(ibset(w,i),j); tmps(IA) = tmps(IA) + U(3,II) * self%s(w)
!           IA = ibset(ibset(w,i),j); tmps(IA) = tmps(IA) + U(4,II) * self%s(w)    
!       enddo
!       self%s = tmps 
!   endsubroutine

!   subroutine runWithGatesFile(self,fileName)
!       implicit none
!       class(Circuit),intent(inout)::self
!       character(*),intent(in)::fileName
!       ! ---------------------------------
!       integer*8::N_gate,gid,Nu,i,j,qi,qj  
!       real*8::rp,ip 
!       complex*16::U2(2,2),U4(4,4)
!       open(999,file=fileName,form='FORMATTED')
!       ! read(999)N_gate
      
!       do while (.True.)
!           read(999,*)Nu
!           ! write(*,*)9995,Nu
!           if ( Nu .eq. 1_8 ) then
!               ! 1 qubit gate
!               read(999,*)qi 
!               do i = 1_8,2_8
!                   do j = 1_8,2_8 
!                       read(999,*)rp 
!                       read(999,*)ip 
!                       U2(i,j) = rp + ip*(0._8,1._8) 
!                   enddo  
!               enddo
!               call self%OneQubitGate(qi,U2) 
!           elseif (Nu.eq.2_8) then 
!               !  2 qubit gate
!               read(999,*)qi 
!               read(999,*)qj
!               ! write(*,*)Nu,666,qi,qj
!               do i = 1_8,4_8
!                   do j = 1_8,4_8 
!                       read(999,*)rp 
!                       read(999,*)ip 
!                       U4(i,j) = rp + ip*(0._8,1._8) 
!                   enddo  
!               enddo
!               ! write(*,*)U4,999
!               call self%TwoQubitGate(qi,qj,U4)
!               ! write(*,*)"here2222"
!           elseif (Nu.eq.-1_8) then 
!               goto 9999
!           endif  
!       enddo 
!  9999 continue
!       close(999)
!   endsubroutine

!   subroutine stdoutMeasurement(self) 
!       implicit none
!       class(Circuit),intent(inout)::self
!       ! ----------------------------
!       integer*8::i 
!       complex*16::v
!       do i = 0_8,self%d-1
!           v = self%s(i)
!           write(*,"(F16.14)") real( v * conjg(v) ) 
!       enddo 
!   endsubroutine


! end module









! Gate ID 
!
!   0    X
!   1    Y
!   2    Z 
!   3    H 
!   4    S 
!   5    T 
!   6    rx
!   7    ry 
!   8    rz
!   9    SD
!   10   TD
!   100   CNOT 
!   101   CZ 

  subroutine gateU4(d,stateIn,stateOut,i,j,U)
      implicit none
      integer*8,intent(in)::d
      complex*16,intent(inout)::stateIn(0:d-1),stateOut(0:d-1)
      integer,intent(in)::i,j 
      complex*16,intent(in)::U(4,4) 
      ! ----------------------
      integer*8::II,IA,IB,w 
      stateOut = (0._8,0._8) 
      Do w = 0, d-1
          if (btest(w,i)) then 
              IA = 1 
          else 
              IA = 0
          endif
          if (btest(w,j)) then 
              IB = 1
          else
              IB = 0 
          endif  
          II = IA * 2 + IB + 1
          IA = ibclr(ibclr(w,i),j); stateOut(IA) = stateOut(IA) + U(1,II) * stateIn(w) 
          IA = ibset(ibclr(w,i),j); stateOut(IA) = stateOut(IA) + U(2,II) * stateIn(w) 
          IA = ibclr(ibset(w,i),j); stateOut(IA) = stateOut(IA) + U(3,II) * stateIn(w)
          IA = ibset(ibset(w,i),j); stateOut(IA) = stateOut(IA) + U(4,II) * stateIn(w)    
      enddo
  endsubroutine

  subroutine gateU2(d,stateIn,stateOut,i,U)
      implicit none
      integer*8,intent(in)::d
      complex*16,intent(inout)::stateIn(0:d-1),stateOut(0:d-1)
      integer,intent(in)::i 
      complex*16,intent(in)::U(2,2)
      ! ----------------------
      complex*16::a,b 
      integer*8::w ,w0,w1 
      stateOut = (0._8,0._8) 
      Do w = 0, d-1 
          ! write(*,*)w,i,999965
          w0 = ibclr( w , i )
          w1 = ibset( w , i ) 
          if (btest( w,i )) then
              a = U(1,2) 
              b = U(2,2)
          else 
              a = U(1,1) 
              b = U(2,1)
          endif 
          stateOut(w0) = stateOut(w0) + a * stateIn(w) 
          stateOut(w1) = stateOut(w1) + b * stateIn(w)  
      enddo
  endsubroutine

subroutine GateOnCircuit(d,iLen,fLen,iPara,fPara,state,wrokSpace,U2,U4)
  integer*8,intent(in)::d 
  integer,intent(in)::iLen,fLen
  integer,intent(in)::iPara(iLen) 
  real*8,intent(in)::fPara(fLen)
  complex*16,intent(inout)::state(d),wrokSpace(d) 
  complex*16,intent(inout)::U2(2,2),U4(4,4)
  !-----------------------------------------------
  complex*16,parameter::Zero = (0._8,0._8)
  complex*16,parameter::One = (1._8,0._8)
  
  ! integer::i
  ! write(*,*)"---- gate on circuit ---" 
  ! do i = 1 , iLen
  !   write(*,*)i,"-th iPara,", iPara(i) 
  ! enddo 

  ! do i = 1 , fLen
  !   write(*,*)i,"-th iPara,", fPara(i) 
  ! enddo 
 
  select case( iPara(1)  )
    case(0)! X
      U2=Zero;U2(2,1)=One;U2(1,2)=One 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(1)! Y 
      U2=Zero;U2(2,1)=(0._8,-1._8);U2(1,2)=(0._8,1._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(2)! Z 
      U2=Zero;U2(1,1)=One;U2(2,2)=-One 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(3)! H 
      U2(1,1)=One;U2(1,2)=One;U2(2,1)=One;U2(2,2)=-One;U2=U2/sqrt(2._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2) 
    case(4)! S
      U2=Zero;U2(1,1)=One;U2(2,2)=(0._8,1._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(5)! T 
      U2=Zero;U2(1,1)=One;U2(2,2)=(1._8,1._8)/sqrt(2._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(6)! Rx 
      U2=Zero
      U2(1,1)=cos( fPara(1)/2._8 )
      U2(1,2)=sin( fPara(1)/2._8 ) * (0._8,-1._8)  
      U2(2,1)=U2(1,2)
      U2(2,2)=U2(1,1)  
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(7)! Ry 
      U2=Zero
      U2(1,1)=cos( fPara(1)/2._8 )
      U2(1,2)=-sin( fPara(1)/2._8 )  
      U2(2,1)=-U2(1,2)
      U2(2,2)=U2(1,1) 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(8)! Rz
      U2=Zero
      U2(1,1)=cos( fPara(1)/2._8 ) - sin( fPara(1)/2._8 )*(0._8,1._8) 
      U2(2,2)=cos( fPara(1)/2._8 ) + sin( fPara(1)/2._8 )*(0._8,1._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2) 
    case(9)! SD
      U2=Zero;U2(1,1)=One;U2(2,2)=(0._8,-1._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(10) !TD
      U2=Zero;U2(1,1)=One;U2(2,2)=(1._8,-1._8)/sqrt(2._8) 
      call gateU2(d,state,wrokSpace,iPara(2),U2)
    case(100) 
      U4=(0._8,0._8);U4(1,1)=(1.0_8,0._8);U4(2,2)=(1.0_8,0._8);U4(3,4)=(1.0_8,0._8);U4(4,3)=(1.0_8,0._8) 
      call gateU4(d,state,wrokSpace,iPara(2),iPara(3),U4) 
    case(101) 
      U4=(0._8,0._8);U4(1,1)=(1.0_8,0._8);U4(2,2)=(1.0_8,0._8);U4(3,3)=(1.0_8,0._8);U4(4,4)=(-1.0_8,0._8) 
      call gateU4(d,state,wrokSpace,iPara(2),iPara(3),U4) 


    case default
      write(*,*)"ERROR: unkonw type of gate"
  endselect 


endsubroutine



subroutine simulateCircuit(d,nGates,intPara,floatPara,OutState)
  implicit none 
  integer*8,intent(in)::d,nGates 
  integer,intent(in)::intPara(:)
  real*8,intent(in)::floatPara(:)
  complex*16,intent(out)::OutState(d)

  complex*16::workspace(d)
  integer,parameter::IntParaLen = 4 
  integer,parameter::floatParaLen = 1
  integer*8::i,itmp1,itmp2 ,itmp3,itmp4 
  complex*16::U2(2,2),U4(4,4)
  logical::isStoredInWorkspace

  isStoredInWorkspace = .False.

  ! write(*,*)"d=",d 
  ! write(*,*)"nGates=",nGates
  ! write(*,*)"intPara=",intPara
  ! write(*,*)"floatPara=",floatPara

  OutState = (0._8,0._8) 
  OutState(1) = (1._8,0._8)

  do i = 1_8,nGates

    ! write(*,*)"Before:gate=",i 
    ! write(*,*)"outstate=",outstate
    ! write(*,*)"workspace=",workspace

    itmp1 = IntParaLen*(i-1) + 1
    itmp2 = itmp1 + IntParaLen - 1  
    itmp3 = floatParaLen*(i-1) + 1
    itmp4 = itmp3 + floatParaLen - 1  
    if (isStoredInWorkspace) then 
      call GateOnCircuit(d,IntParaLen,floatParaLen,intPara(itmp1:itmp2),floatPara(itmp3:itmp4),workspace,OutState,U2,U4)
    else 
      call GateOnCircuit(d,IntParaLen,floatParaLen,intPara(itmp1:itmp2),floatPara(itmp3:itmp4),OutState,workspace,U2,U4)
    endif 
    isStoredInWorkspace = .not. isStoredInWorkspace

    ! write(*,*)"After:gate=",i 
    ! write(*,*)"outstate=",outstate
    ! write(*,*)"workspace=",workspace

  enddo 

  if (isStoredInWorkspace) then
    OutState = workspace
  endif 


  ! write(*,*)"final Output="
  ! write(*,*)OutState
endsubroutine 


! program main
!   implicit none 

! endprogram






















!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! Following is a better one in pure Fortran env.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





! module mod_Circuit 
!   implicit none 


!   type,public::Circuit
!       private
!       logical::initialized = .False.
!       integer*8::Nq 
!       integer*8::d 
!       complex*16,allocatable::S(:)

!       contains
!           procedure,pass::Initialization 
!           procedure,pass::getState
!           procedure,pass::OneQubitGate => U2 
!           procedure,pass::TwoQubitGate => U4 
!           procedure,pass::runWithGatesFile
!           procedure,pass::stdoutMeasurement
!   endtype

!   private::Initialization
!   private::getState
!   private::U2,U4 
!   private::runWithGatesFile
!   private::stdoutMeasurement

!   contains

!   subroutine Initialization(self,Nq)
!       implicit none 
!       class(Circuit),intent(inout)::self
!       integer*8,intent(in)::Nq 
!       ! --------------------------
!       if (self%initialized) deallocate(self%S) 
!       self%initialized = .True. 
!       self%Nq = Nq 
!       allocate(self%S(0:2_8**self%Nq-1_8))
!       self%S = (0._8,0._8) 
!       self%S(0) = (1._8,0._8)
!       self%d = 2_8**self%Nq 
!   endsubroutine


!   function getState(self) result(state)
!       implicit none 
!       class(Circuit),intent(inout)::self
!       complex*16::state(self%d) 
!       ! ---------------------------
!       state = self%s
!   endfunction

!   subroutine U2(self,i,U)
!       implicit none
!       class(Circuit),intent(inout)::self
!       integer*8,intent(in)::i 
!       complex*16,intent(in)::U(2,2) 
!       ! ----------------------
!       complex*16::tmpS(0:self%d-1),a,b 
!       integer*8::w ,w0,w1 
!       tmpS = (0._8,0._8) 
!       Do w = 0, self%d-1_8 
!           ! write(*,*)w,i,999965
!           w0 = ibclr( w , i )
!           w1 = ibset( w , i ) 
!           if (btest( w,i )) then
!               a = U(1,2) 
!               b = U(2,2)
!           else 
!               a = U(1,1) 
!               b = U(2,1)
!           endif 
!           tmpS(w0) = tmpS(w0) + a * self%s(w) 
!           tmpS(w1) = tmpS(w1) + b * self%s(w)  
!       enddo
!       self%s = tmps 
!   endsubroutine

!   subroutine U4(self,i,j,U)
!       implicit none
!       class(Circuit),intent(inout)::self
!       integer*8,intent(in)::i,j 
!       complex*16,intent(in)::U(4,4) 
!       ! ----------------------
!       complex*16::tmpS(0:self%d-1) 
!       integer*8::II,IA,IB,w 
!       tmpS = (0._8,0._8) 
!       Do w = 0, self%d-1_8
!           if (btest(w,i)) then 
!               IA = 1_8 
!           else 
!               IA = 0_8 
!           endif
!           if (btest(w,j)) then 
!               IB = 1_8
!           else
!               IB = 0_8 
!           endif  
!           II = IA * 2 + IB + 1_8 
!           IA = ibclr(ibclr(w,i),j); tmpS(IA) = tmpS(IA) + U(1,II) * self%s(w) 
!           IA = ibset(ibclr(w,i),j); tmps(IA) = tmps(IA) + U(2,II) * self%s(w) 
!           IA = ibclr(ibset(w,i),j); tmps(IA) = tmps(IA) + U(3,II) * self%s(w)
!           IA = ibset(ibset(w,i),j); tmps(IA) = tmps(IA) + U(4,II) * self%s(w)    
!       enddo
!       self%s = tmps 
!   endsubroutine

!   subroutine runWithGatesFile(self,fileName)
!       implicit none
!       class(Circuit),intent(inout)::self
!       character(*),intent(in)::fileName
!       ! ---------------------------------
!       integer*8::N_gate,gid,Nu,i,j,qi,qj  
!       real*8::rp,ip 
!       complex*16::U2(2,2),U4(4,4)
!       open(999,file=fileName,form='FORMATTED')
!       ! read(999)N_gate
      
!       do while (.True.)
!           read(999,*)Nu
!           ! write(*,*)9995,Nu
!           if ( Nu .eq. 1_8 ) then
!               ! 1 qubit gate
!               read(999,*)qi 
!               do i = 1_8,2_8
!                   do j = 1_8,2_8 
!                       read(999,*)rp 
!                       read(999,*)ip 
!                       U2(i,j) = rp + ip*(0._8,1._8) 
!                   enddo  
!               enddo
!               call self%OneQubitGate(qi,U2) 
!           elseif (Nu.eq.2_8) then 
!               !  2 qubit gate
!               read(999,*)qi 
!               read(999,*)qj
!               ! write(*,*)Nu,666,qi,qj
!               do i = 1_8,4_8
!                   do j = 1_8,4_8 
!                       read(999,*)rp 
!                       read(999,*)ip 
!                       U4(i,j) = rp + ip*(0._8,1._8) 
!                   enddo  
!               enddo
!               ! write(*,*)U4,999
!               call self%TwoQubitGate(qi,qj,U4)
!               ! write(*,*)"here2222"
!           elseif (Nu.eq.-1_8) then 
!               goto 9999
!           endif  
!       enddo 
!  9999 continue
!       close(999)
!   endsubroutine

!   subroutine stdoutMeasurement(self) 
!       implicit none
!       class(Circuit),intent(inout)::self
!       ! ----------------------------
!       integer*8::i 
!       complex*16::v
!       do i = 0_8,self%d-1
!           v = self%s(i)
!           write(*,"(F16.14)") real( v * conjg(v) ) 
!       enddo 
!   endsubroutine
! end module
